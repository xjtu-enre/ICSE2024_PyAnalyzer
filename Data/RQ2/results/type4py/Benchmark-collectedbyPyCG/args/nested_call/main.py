def nested_func():
    pass


def param_func(a: int):
    a()


def func(a: int):
    a(nested_func)


b = param_func
c = func
c(b)
