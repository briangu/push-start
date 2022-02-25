import importlib
import sys
import typing

import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web
from pysyncobj import SyncObjConsumer, replicated
from pysyncobj.batteries import ReplList
from tornado.routing import Router

from pushpy.batteries import ReplEventDict, ReplVersionedDict, ReplTaskManager
from pushpy.code_store import load_src, CodeStoreLoader
from pushpy.push_manager import PushManager
from pushpy.task_manager import TaskManager


class Handle404(tornado.web.RequestHandler):
    def get(self):
        self.set_status(404)
        self.write('404 Not Found')


# https://stackoverflow.com/questions/47970574/tornado-routing-to-a-base-handler
class MyRouter(Router):
    def __init__(self, store, app, prefix=None):
        self.store = store
        self.app = app
        self.prefix = prefix or '/web'

    def find_handler(self, request, **kwargs):
        host = request.headers.get("Host")

        try:
            handler = load_src(self.store, f"{self.prefix}/{host}{request.path}") or Handle404
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(e)
            handler = Handle404

        return self.app.get_handler_delegate(request, handler)


def make_app(kvstore):
    return MyRouter(kvstore, tornado.web.Application())


# TODO: this could be a replicated command ReplLambda / ReplCommand that runs on all hosts
class DoRegister:
    def __init__(self, store):
        self.store = store

    def apply(self, name, src):
        src = load_src(self.store, src)
        q = src()
        PushManager.register(name, callable=lambda l=q: l)


def main() -> (typing.List[object], typing.Dict[str, object]):
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
    boot_globals['repl_kvstore'] = repl_kvstore
    boot_globals['repl_ver_store'] = repl_ver_store
    boot_globals['repl_code_store'] = repl_code_store
    boot_globals['repl_tasks'] = repl_task_manager
    boot_globals['local_tasks'] = tm
    boot_globals['local_register'] = DoRegister(repl_code_store)
    boot_globals['repl_strategies'] = repl_strategies

    tm.start_event_handlers()

    return boot_globals, make_app(repl_code_store)
