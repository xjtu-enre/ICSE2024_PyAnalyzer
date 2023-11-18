def func2():
    pass


def func(key: str='a'):
    d[key] = func2


d = {}
func()
d['a']()
