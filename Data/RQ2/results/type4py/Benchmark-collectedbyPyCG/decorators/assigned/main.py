def dec1(f: BinaryIO) ->int:
    return f


def dec2(f: BinaryIO) ->int:
    return f


a = dec1
a = dec2


@a
def func():
    pass


func()
