from ex_push_manager import ExamplePushManager

# https://stackoverflow.com/questions/52402783/pickle-class-definition-in-module-with-dill

class Multiplier:
    def apply(self, a, b):
        return a * b


class Adder:
    def apply(self, a, b):
        return a + b


class Interpreter:
    def apply(self, ops, i=None):
        from interpreter.math import Adder, Multiplier
        i = 0 if i is None else i
        while i < len(ops):
            op = ops[i]
            i += 1
            if op == "add":
                a, i = self.apply(ops, i)
                b, i = self.apply(ops, i)
                return Adder().apply(a, b), i
            elif op == "mul":
                a, i = self.apply(ops, i)
                b, i = self.apply(ops, i)
                return Multiplier().apply(a, b), i
            else:
                return op, i


m = ExamplePushManager()
m.connect()

local_tasks = m.local_tasks()

repl_code_store = m.repl_code_store()
repl_code_store.update({
    "interpreter.Interpreter": Interpreter,
    "interpreter.math.Adder": Adder,
    "interpreter.math.Multiplier": Multiplier
}, sync=True)

ops = ['add', 'add', 1, 2, 'mul', 3, 4]

def run_interp(x):
    from interpreter import Interpreter
    return Interpreter().apply(x)

# run task via this client
r = local_tasks.apply(run_interp, ops)[0]
print(r)
assert r == 15

repl_code_store.set("run_interp", run_interp, sync=True)
r = local_tasks.apply("run_interp", ops)[0]
print(r)
assert r == 15

class Adder2(Adder):
    def apply(self, a, b):
        print("using adder v2")
        return (a + b) * 2

repl_code_store.set("interpreter.math.Adder", Adder2, sync=True)
r = local_tasks.apply("interpreter.Interpreter", ops)[0]
print(r)
assert r == 36

r = local_tasks.apply("run_interp", ops)[0]
print(r)
assert r == 36

class InterpreterWrapper:
    def apply(self, ops):
        print("InterpreterWrapper")
        from interpreter import Interpreter
        return Interpreter().apply(ops)


r = local_tasks.apply(InterpreterWrapper, ops)[0]
print(r)
assert r == 36
