class Base:
    static_attr = 1
    def __init__(self):
        self.base_attribute = 1

class Inherit(Base):
    def __init__(self):

        super().__init__()

    def use_attribute(self):
        self.base_attribute = 1

        self.static_attr = 2

Base.static_attr = 2