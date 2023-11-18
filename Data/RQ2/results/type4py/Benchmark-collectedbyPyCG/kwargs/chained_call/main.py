def func3():
    pass


def func2(a: int=func3):
    a()


def func1(a: int, b: int=func2):
    a(b)


func1(a=func2, b=func3)
