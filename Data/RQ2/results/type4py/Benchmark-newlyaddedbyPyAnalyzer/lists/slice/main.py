def func1():
    pass


def func2():
    pass


def func3():
    pass


ls = [func1, func2, func3]


def func(l: int):
    ls2 = l[1:3]
    ls2[0]()


func(ls)
