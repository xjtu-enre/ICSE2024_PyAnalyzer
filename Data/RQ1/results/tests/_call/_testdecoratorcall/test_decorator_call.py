def f1(a):
    def wrap(f):
        return f
    return wrap

def f2(f):
    return f

@f1(arg)
@f2
def func(): pass