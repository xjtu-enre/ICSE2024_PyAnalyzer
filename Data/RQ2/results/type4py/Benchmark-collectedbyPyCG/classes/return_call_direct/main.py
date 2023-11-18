class MyClass:

    def func2(self):
        pass

    def func1(self) ->Callable:
        return self.func2


a = MyClass()
a.func1()()
