def create_class():
    class Simple:
        def method(self):
            ...

    return Simple


cls = create_class()
obj = cls()
obj.method()
