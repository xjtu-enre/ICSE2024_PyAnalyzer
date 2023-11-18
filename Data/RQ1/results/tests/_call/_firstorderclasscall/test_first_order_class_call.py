class Base:
    ...

base = Base()

def create_class():
    class Difficult:
        def test(self):
            ...
    return Difficult

cls = create_class()

difficult_obj = cls()

difficult_obj.test()