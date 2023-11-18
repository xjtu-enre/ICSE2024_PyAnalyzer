class Base:
    static_attr = 1
    def __init__(self):
        self.base_attribute = 1

class Inherit(Base):
    def __init__(self):

        super().__init__()

    def use_attribute(self):
        print(self.base_attribute)

        print(self.static_attr)

print(Base.static_attr)

class Foo:
    static_attr = Base.static_attr
