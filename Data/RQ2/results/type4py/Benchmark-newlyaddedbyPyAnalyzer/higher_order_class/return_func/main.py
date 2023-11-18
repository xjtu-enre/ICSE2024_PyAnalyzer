def create_class() ->str:

    def fun():
        ...


    class Simple:

        def method(self) ->str:
            return fun
    return Simple


cls = create_class()
obj = cls()
func = obj.method()
func()
