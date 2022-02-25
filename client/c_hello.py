import tornado.web
import sys

from ex_push_manager import ExamplePushManager

m = ExamplePushManager()
m.connect()

repl_code_store = m.repl_code_store()

host = sys.argv[1] if len(sys.argv) > 1 else "localhost:10000"

# curl localhost:11000/
class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        from boot_common import repl_code_store
        self.write(f"hello, world!!!! [{repl_code_store.get_head()}]\n")


repl_code_store.set(f"/web/{host}/", HelloWorldHandler, sync=True)
