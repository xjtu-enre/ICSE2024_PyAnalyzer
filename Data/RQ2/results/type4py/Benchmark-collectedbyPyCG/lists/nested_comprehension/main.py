def func1(a: int) ->str:
    return a + 1


def func2(a: int) ->str:
    return a + 1


[func1(a) for a in [func2(b) for b in range(10)]]
