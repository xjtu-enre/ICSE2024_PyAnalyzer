def func1():
    pass


def func2():
    pass


def func3():
    pass


ls = [func1, func2, func3]


def func(l: list):
    for f in l:
        f()


func(ls)
