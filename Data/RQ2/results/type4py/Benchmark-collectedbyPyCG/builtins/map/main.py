def func(x: int):
    pass


map([1, 2, 3], func)


def func2(x: Union[int, float]) ->Callable:
    return func(x)


map([1, 2, 3], func2)


def func3(x: int) ->Callable:

    def func():
        return x
    return func


res = map([1, 2, 3], func3)
for r in res:
    r()
