def dec(f: BinaryIO) ->int:
    return f


def func():

    def dec(f: BinaryIO) ->int:
        return f

    @dec
    def inner():
        pass


func()
