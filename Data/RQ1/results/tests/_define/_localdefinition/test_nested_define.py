
def func():


    def inner():


        def inner_inner():


            func()

        func()


        inner_inner()

    inner()

def func2():

    x = 1


    y: int = 1


    t1, t2 = 1, 2




    (t3 := 1)

