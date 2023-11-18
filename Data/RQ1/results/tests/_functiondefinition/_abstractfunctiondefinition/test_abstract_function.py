from abc import ABC, abstractmethod


class Foo(ABC):
    @abstractmethod
    def foo1(self):
        pass

    @abstractmethod
    def foo2(self):
        pass

    def foo3(self):
        ...
