def func(c: bool):
    for i in c:
        pass


class Cls:

    def __init__(self, max: int=0):
        self.max = max

    def __iter__(self) ->int:
        self.n = 0
        return self

    def __next__(self) ->Optional[Any]:
        if self.n > self.max:
            raise StopIteration
        result = 2 ** self.n
        self.n += 1
        return func


func(Cls())
