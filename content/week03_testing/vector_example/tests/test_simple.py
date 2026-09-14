from vector import Vector

import pytest


def test_vector_ops():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    assert v1 + v2 == Vector(4, 6)
    assert v1 - v2 == Vector(-2, -2)
    assert v1.mag() == pytest.approx(2.23606797749979)
    assert v2.mag() == pytest.approx(5.0)


def test_vector_repr():
    v = Vector(1, 2)
    assert repr(v) == "Vector(1, 2)"


def test_vector_eq():
    v1 = Vector(1, 2)
    v2 = Vector(1, 2)
    assert v1 == v2
