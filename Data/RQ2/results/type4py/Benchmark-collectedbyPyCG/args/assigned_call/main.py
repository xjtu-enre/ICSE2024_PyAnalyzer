def param_func():
    pass


def func(a: int):
    a()


b = param_func
func(b)
