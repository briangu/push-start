import os
import sys
from ex_push_manager import ExamplePushManager

m = ExamplePushManager()
m.connect()

repl_code_store = m.repl_code_store()


def list_files(startpath):
    wd = {}
    for root, dirs, files in os.walk(startpath):
        for fname in files:
            p = os.path.join(root, fname)
            with open(p, "rb") as f:
                d = f.read()
                print(f"{len(d)}\t{p}")
                wd[p] = d
    return wd


start_dir = sys.argv[1] if len(sys.argv) > 1 else "web"

web_dict = list_files('web')

repl_code_store.update(web_dict, sync=True)
