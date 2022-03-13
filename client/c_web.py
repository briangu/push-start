import os
import sys
import dill
import pickle
from ex_push_manager import ExamplePushManager

m = ExamplePushManager()
m.connect()

repl_code_store = m.repl_code_store()


class FileObject:
    def __init__(self, o):
        self.o = o


def list_files(startpath):
    wd = {}
    for root, dirs, files in os.walk(startpath):
        for fname in files:
            p = os.path.join(root, fname)
            if fname == 'index.html':
                k = f"{root}/"
            else:
                k = p
            k = f"/{k}"
            with open(p, "rb") as f:
                d = f.read()
                v = dill.dumps(d)
                q = dill.loads(v)
                assert d == q
                assert q == pickle.loads(pickle.dumps(q))
                print(f"{len(d)}\t{len(v)}\t{k} {type(v)}")
                wd[k] = v
                print(type(v))
#                try:
#                repl_code_store.set(k, v, sync=True)
#                except Exception as e:
#                    print(e)
    return wd


start_dir = sys.argv[1] if len(sys.argv) > 1 else "web"

web_dict = list_files('web')
print(list(web_dict.keys()))
repl_code_store.update(web_dict, sync=True)

