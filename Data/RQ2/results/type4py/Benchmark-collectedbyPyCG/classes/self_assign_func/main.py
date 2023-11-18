class A:

    def func(self):
        pass


class B:

    def __init__(self, a: int):
        self.a = a

    def func(self):
        self.a.func()


a = A()
b = B(a)
b.func()
