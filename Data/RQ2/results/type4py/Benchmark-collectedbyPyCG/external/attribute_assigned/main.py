from ext import Cls


def fn(a: List[T]):
    a()


a = Cls()
fn(a.fun)
