def func():
    pass


def func2(a: int) ->str:
    return a


def func3() ->Callable:
    return func2


func3()(func)()
