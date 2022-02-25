import os
import sys
import dill
from ex_push_manager import ExamplePushManager

m = ExamplePushManager()
m.connect()

repl_code_store = m.repl_code_store()


def list_files(startpath):
    wd = {}
    for root, dirs, files in os.walk(startpath):
        for fname in files:
            p = os.path.join(root, fname)
            if fname == 'index.html':
                k = root + os.path.sep #os.path.join(root, os.path.sep)
            else:
                k = p
            k = f"/{k}"
            with open(p, "rb") as f:
                d = f.read()
#                print(type(dill.loads(dill.dumps(d))))
                print(f"{len(d)}\t{k}")
                wd[k] = dill.dumps(d)
    return wd


start_dir = sys.argv[1] if len(sys.argv) > 1 else "web"

web_dict = list_files('web')
print(list(web_dict.keys()))

repl_code_store.update(web_dict, sync=True)
