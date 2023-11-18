def func(a: int) ->str:
    return a + 1


ls = [func(a) for a in range(10)]
