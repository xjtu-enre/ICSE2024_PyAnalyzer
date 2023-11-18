def func1() ->bytes:

    def dec(f: BinaryIO) ->int:
        return f
    return dec


@func1()
def func2():
    pass


func2()
