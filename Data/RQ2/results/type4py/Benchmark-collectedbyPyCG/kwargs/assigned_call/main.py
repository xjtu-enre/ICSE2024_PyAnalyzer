def func2():
    pass


def func(a: int):
    a()


a = func
b = func2
a(a=b)
