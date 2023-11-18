class MyClass:

    def func3(self):
        pass

    def func2(self, a: int):
        a()

    def func1(self, a: int, b: int):
        a(b)


a = MyClass()
a.func1(a.func2, a.func3)
