
import math

import pytest

from gmtry import Triangle


def test_right_triangle():
    triangle = Triangle(3, 4, 5)

    assert triangle.is_right
    assert triangle.is_scalene
    assert triangle.area == pytest.approx(6)
    assert triangle.perimeter == pytest.approx(12)
    assert triangle.circumradius == pytest.approx(2.5)


def test_equilateral_triangle():
    triangle = Triangle(5, 5, 5)

    assert triangle.is_equilateral
    assert triangle.is_isosceles
    assert triangle.is_acute
    assert triangle.angles == pytest.approx((60, 60, 60))


def test_obtuse_triangle():
    triangle = Triangle(5, 5, 8)

    assert triangle.is_isosceles
    assert triangle.is_obtuse
    assert not triangle.is_right
    assert triangle.area == pytest.approx(12)


def test_invalid_triangle():
    with pytest.raises(ValueError):
        Triangle(1, 2, 3)


def test_non_positive_side():
    with pytest.raises(ValueError):
        Triangle(0, 2, 2)


def test_invalid_type():
    with pytest.raises(TypeError):
        Triangle("3", 4, 5)


def test_triangle_equality():
    assert Triangle(3, 4, 5) == Triangle(5, 3, 4)
    assert Triangle(3, 4, 5) != Triangle(4, 4, 5)


def test_angles_sum_to_180():
    triangle = Triangle(5, 6, 7)

    assert math.fsum(triangle.angles) == pytest.approx(180)
