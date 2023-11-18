def func():
    ...

x = [1]
foo = func

for a in x:
    def foo():
        ...


foo()
