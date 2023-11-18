from abc import abstractmethod, ABCMeta, ABC


class A(ABC):
    ...


class B:
    class Inner:
        __metaclass__ = ABCMeta

        @abstractmethod
        def __init__(self):
            if self.__class__.__name__ == "Inner":
                raise NotImplementedError("You can't instantiate this abstract class. Derive it, please.")

        @abstractmethod
        def __new__(cls):
            if cls.__class__.__name__ == "Inner":
                raise NotImplementedError("You can't instantiate this abstract class. Derive it, please.")

        @abstractmethod
        def func1(self):
            pass

        def func2(self):
            ...

    @abstractmethod
    def func3(self):
        ...
