def func() ->str:
    return 1 + 1


func()


def func2() ->str:
    return 1


def func3() ->Callable:
    return func2


def func4(a: int) ->Callable:
    return func3()


func4()()


def func5() ->Callable:
    return func2() + 1


func5()
