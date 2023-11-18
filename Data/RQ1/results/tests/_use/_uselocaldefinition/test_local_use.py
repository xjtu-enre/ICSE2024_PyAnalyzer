def func():

    def inner():

        def inner_inner():
            print(func)

        print(func)
        print(inner_inner)

    print(inner)

def func2(p):

    x = 1

    y: int = 1

    t1, t2 = 1, 2

    (t3 := 1)

    for a, b in x:
        print(a)
        print(b)

    print(x)

    print(y)
    print(t1)

    print(t2)
    print(t3)

    print(p)