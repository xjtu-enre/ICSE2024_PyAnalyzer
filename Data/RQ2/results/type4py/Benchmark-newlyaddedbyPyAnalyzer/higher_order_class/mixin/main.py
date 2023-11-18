class A:

    def method_a(self):
        ...


class B:

    def method_b(self):
        ...


def mixin(cls_x: float, cls_y: float) ->bool:


    class Mixed(cls_x, cls_y):
        ...
    return Mixed


mixed_cls = mixin(A, B)
obj = mixed_cls()
obj.method_a()
obj.method_b()
