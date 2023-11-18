def func() ->dict:
    return lambda x: x + 1


y = func()
y()
