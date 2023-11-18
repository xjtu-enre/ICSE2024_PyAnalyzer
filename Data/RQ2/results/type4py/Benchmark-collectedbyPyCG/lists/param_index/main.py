def func2():
    pass


def func1(key: str):
    ls[key]()


ls = [func1, func2]
func1(1)
