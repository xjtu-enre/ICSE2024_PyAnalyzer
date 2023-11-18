def func(a: int):
    a()


def func2() ->Callable:
    return func3


def func3():
    pass


func(func2())
