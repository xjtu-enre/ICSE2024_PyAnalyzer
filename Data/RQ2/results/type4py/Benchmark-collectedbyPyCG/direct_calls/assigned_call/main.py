def return_func():
    pass


def func() ->str:
    a = return_func
    return a


a = func
a()()
