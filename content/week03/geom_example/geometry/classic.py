import dataclasses
import abc
import math


class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self):
        pass

    @abc.abstractmethod
    def perimeter(self):
        pass


@dataclasses.dataclass
class Triangle:
    a: float
    b: float
    c: float

    def area(self):
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5

    def perimeter(self):
        return self.a + self.b + self.c


@dataclasses.dataclass
class Rectagle(Shape):
    width: float
    height: float

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Square(Rectagle):
    def __init__(self, side):
        super().__init__(side, side)

    def __repr__(self):
        return f"{self.__class__.__name__}(side={self.width})"


@dataclasses.dataclass
class Circle(Shape):
    radius: float

    def __post_init__(self):
        assert self.radius >= 0, "Radius must be non-negative"

    def area(self):
        return math.pi * self.radius**2

    def perimeter(self):
        return math.tau * self.radius
