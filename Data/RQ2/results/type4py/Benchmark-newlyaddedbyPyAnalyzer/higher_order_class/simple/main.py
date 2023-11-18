def create_class() ->str:


    class Simple:

        def method(self):
            ...
    return Simple


cls = create_class()
obj = cls()
obj.method()
