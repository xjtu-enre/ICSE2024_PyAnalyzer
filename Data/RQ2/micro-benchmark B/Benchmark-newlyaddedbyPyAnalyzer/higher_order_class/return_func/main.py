def create_class():
    def fun():
        ...

    class Simple:
        def method(self):
            return fun

    return Simple


cls = create_class()
obj = cls()
func = obj.method()
func()
