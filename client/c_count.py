import tornado.web
import sys

from ex_push_manager import ExamplePushManager

m = ExamplePushManager()
m.connect()

repl_counter = m.repl_counter()

n = 1 if len(sys.argv) == 1 else int(sys.argv[1])

for i in range(n):
    print(f"inc: {i}")
    repl_counter.inc()
