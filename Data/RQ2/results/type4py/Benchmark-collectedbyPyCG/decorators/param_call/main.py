def dec(f: BinaryIO) ->int:
    f()
    return f


@dec
def func():
    pass


func()
