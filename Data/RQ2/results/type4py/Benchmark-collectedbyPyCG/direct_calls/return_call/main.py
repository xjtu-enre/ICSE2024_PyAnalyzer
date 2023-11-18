def return_func() ->str:

    def nested_return_func():
        pass
    return nested_return_func


def func() ->Type[Any]:
    return return_func


func()()
func()()()
