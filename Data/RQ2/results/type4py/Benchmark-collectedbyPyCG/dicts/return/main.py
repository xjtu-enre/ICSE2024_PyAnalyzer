def func2():
    pass


def func1() ->Dict[str, str]:
    d = {'a': func2}
    return d


b = func1()
b['a']()
