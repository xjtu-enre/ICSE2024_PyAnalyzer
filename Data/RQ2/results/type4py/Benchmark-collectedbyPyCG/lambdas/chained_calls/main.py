def func3(a: int):
    a()


def func2(a: int, b: float):
    a()
    func3(b)


def func1(a: int, b: int, c: int):
    a()
    func2(b, c)


func1(lambda x: x + 1, lambda x: x + 2, lambda x: x + 3)
