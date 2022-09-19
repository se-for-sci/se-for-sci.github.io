from geometry.classic import Rectagle, Square, Circle, Triangle
import math
from pytest import approx


def test_triangle():
    t = Triangle(3, 4, 5)
    assert t.area() == 6
    assert t.perimeter() == 12


def test_rectangle():
    r = Rectagle(3, 4)
    assert r.area() == 12
    assert r.perimeter() == 14


def test_square():
    s = Square(4)
    assert s.area() == 16
    assert s.perimeter() == 16


def test_circle():
    c = Circle(2)
    assert c.area() == approx(math.pi * 4)
    assert c.perimeter() == approx(math.pi * 2 * 2)
