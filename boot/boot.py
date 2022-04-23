import importlib
import sys
import os
import typing

import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web
from pysyncobj import replicated
from pysyncobj.batteries import ReplCounter, ReplList
from tornado.routing import Router
import mimetypes

from pushpy.batteries import ReplEventDict, ReplVersionedDict, ReplTaskManager
from pushpy.code_store import load_src, CodeStoreLoader
from pushpy.push_manager import PushManager
from pushpy.task_manager import TaskManager


class Handle404(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.set_status(404)
        self.write('404 Not Found')


class GetResource(tornado.web.RequestHandler):
#    def __init__(self, *args, data=None):
#        self.data = data

    def initialize(self, data):
        self.data = data

    def get(self, path, **kwargs):
        print(f"get: {path}")
        bn = os.path.basename(path)
        mt = mimetypes.guess_type(bn)[0]
        print(f"basename: {bn} mt: {mt}")
        if mt is not None:
            self.set_header("Content-Type", mt)
        self.write(self.data)


# https://stackoverflow.com/questions/47970574/tornado-routing-to-a-base-handler
class MyRouter(Router):
    def __init__(self, store, app, prefix=None):
        self.store = store
        self.app = app
        self.prefix = prefix or '/web'

    def find_handler(self, request, **kwargs):
        host = request.headers.get("Host")
        p = f"{self.prefix}/{host}{request.path}"
        target_kwargs = {} 
        try:
            handler = load_src(self.store, p) or Handle404
            is_bytes = isinstance(handler, bytes)
            if is_bytes: 
                target_kwargs = {'data': handler} 
                handler = GetResource 
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(e)
            handler = Handle404

        return self.app.get_handler_delegate(request, handler, target_kwargs=target_kwargs, path_args=[p])


def make_router(code_store, template_store):
    app = tornado.web.Application(template_loader=tornado.template.DictLoader(template_store))
    return MyRouter(code_store, app)


class MyReplCounter(ReplCounter):

    @replicated
    def inc(self):
        p = self.get()
        super().inc(_doApply=True)
        print(f"inc: {p} -> {self.get()}")


# TODO: this could be a replicated command ReplLambda / ReplCommand that runs on all hosts
class DoRegister:
    def __init__(self, store):
        self.store = store

    def apply(self, name, src):
        src = load_src(self.store, src)
        q = src()
        PushManager.register(name, callable=lambda l=q: l)


def main() -> (typing.List[object], typing.Dict[str, object]):
    repl_counter = MyReplCounter()
    repl_code_store = ReplVersionedDict()
    tm = TaskManager(repl_code_store)
    repl_ver_store = ReplVersionedDict()
    repl_kvstore = ReplEventDict(on_set=tm.on_event_handler("process_kv_updates"))
    repl_strategies = ReplList()
    repl_task_manager = ReplTaskManager(repl_kvstore, tm)

    # the code store will be directly used for imports, where the keys are the resolvable package names
    finder = CodeStoreLoader.install(repl_code_store)

    def invalidate_caches(head):
        print(f"reloading push modules: head={head}")
        finder.invalidate_caches()
        repl_packages = set(finder.cache_store.keys())
        # TODO: reloading modules that may run against modules that are still old has to have problems at some point
        #       do we just flush them out of sys.modules and reload on demand?
        for key in list(sys.modules.keys()):
            pkg = key.split(".")[0]
            if pkg in repl_packages:
                importlib.reload(sys.modules[key])
                print(f"reloading module: {key}")

    repl_code_store.on_head_change = invalidate_caches

    boot_globals = dict()
    boot_globals['repl_counter'] = repl_counter
    boot_globals['repl_kvstore'] = repl_kvstore
    boot_globals['repl_ver_store'] = repl_ver_store
    boot_globals['repl_code_store'] = repl_code_store
    boot_globals['repl_tasks'] = repl_task_manager
    boot_globals['local_tasks'] = tm
    boot_globals['local_register'] = DoRegister(repl_code_store)
    boot_globals['repl_strategies'] = repl_strategies

    tm.start_event_handlers()

    return boot_globals, make_router(repl_code_store, repl_ver_store)
