from ex_push_manager import ExamplePushManager

class ShowGlobals:
    def apply(self):
        return list(globals().keys())


class ShowLocals:
    def apply(self):
        # show that we can use boot_common to import some instances
        from boot_common import repl_ver_store
        return list(locals().keys())

m = ExamplePushManager()
m.connect()


local_tasks = m.local_tasks()

class MainShowGlobals:
    def apply(self):
        return list(globals().keys())

class MainShowLocals:
    def apply(self):
        from boot_common import host_id
        return list(locals().keys())


print("Globals in the lambda context")
print(local_tasks.apply(lambda: host_id))
print()


print("Globals in this __main__ context")
print(local_tasks.apply(MainShowGlobals))
print()
print("Locals in this __main__ context method")
print(local_tasks.apply(MainShowLocals))
print()

print("globals in the ShowGlobals module")
print(local_tasks.apply(ShowGlobals))
print()
print("locals in the ShowLocals apply method")
print(local_tasks.apply(ShowLocals))
