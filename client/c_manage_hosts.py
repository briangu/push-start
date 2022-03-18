import tornado.web
import sys

from ex_push_manager import ExamplePushManager

host = sys.argv[1]
cmd = sys.argv[2]
params = sys.argv[3:]

m = ExamplePushManager(host=host)
m.connect()

sync_obj = m.sync_obj()

if cmd == "add":
    print(f"adding node: {params[0]}")
    sync_obj.addNodeToCluster(params[0])
elif cmd == "rm":
    print(f"removing node: {params[0]}")
    sync_obj.removeNodeFromCluster(params[0])
elif cmd == "status":
    status: dict = sync_obj.getStatus()
    for k, v in status.items():
        print(f'{str(k)}, {str(v)}')


