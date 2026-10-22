
import math

import pytest

from gmtry import (
    Quadrilateral,
    Rectangle,
    Rhombus,
    Parallelogram,
    Square,
    Trapezoid,
)


# Quadrilateral

def test_quadrilateral_basic_properties():
    quad = Quadrilateral(3, 4, 5, 6, diagonal_ac=5)

    assert quad.sides == (3, 4, 5, 6)
    assert quad.perimeter == pytest.approx(18)
    assert quad.area > 0
    assert quad.is_convex
    assert len(quad.angles) == 4
    assert len(quad.diagonals) == 2


def test_quadrilateral_angles_sum_to_360():
    quad = Quadrilateral(3, 4, 5, 6, diagonal_ac=5)

    assert sum(quad.angles) == pytest.approx(360)


def test_quadrilateral_diagonals_are_positive():
    quad = Quadrilateral(3, 4, 5, 6, diagonal_ac=5)

    assert all(diagonal > 0 for diagonal in quad.diagonals)


def test_quadrilateral_invalid_diagonal():
    with pytest.raises(ValueError):
        Quadrilateral(3, 4, 5, 6, diagonal_ac=20)


def test_quadrilateral_invalid_side():
    with pytest.raises(ValueError):
        Quadrilateral(0, 4, 5, 6, diagonal_ac=5)


def test_quadrilateral_rejects_boolean_side():
    with pytest.raises(TypeError):
        Quadrilateral(True, 4, 5, 6, diagonal_ac=5)


def test_quadrilateral_rejects_non_finite_side():
    with pytest.raises(ValueError):
        Quadrilateral(3, 4, 5, math.inf, diagonal_ac=5)


# Rectangle

def test_rectangle_properties():
    rectangle = Rectangle(8, 4)

    assert rectangle.area == pytest.approx(32)
    assert rectangle.perimeter == pytest.approx(24)
    assert rectangle.classification == "rectangle"
    assert rectangle.is_rectangle
    assert rectangle.is_parallelogram
    assert not rectangle.is_square
    assert rectangle.angles == pytest.approx((90, 90, 90, 90))


def test_rectangle_diagonals_are_equal():
    rectangle = Rectangle(8, 4)

    assert rectangle.diagonals[0] == pytest.approx(math.sqrt(80))
    assert rectangle.diagonals[1] == pytest.approx(math.sqrt(80))


def test_rectangle_dimensions():
    rectangle = Rectangle(8, 4)

    assert rectangle.length == 8
    assert rectangle.width == 4


# Square

def test_square_properties():
    square = Square(5)

    assert square.area == pytest.approx(25)
    assert square.perimeter == pytest.approx(20)
    assert square.classification == "square"
    assert square.is_square
    assert square.is_rectangle
    assert square.is_rhombus
    assert square.is_parallelogram
    assert square.is_equilateral


def test_square_diagonal():
    square = Square(5)

    assert square.diagonal_ac == pytest.approx(5 * math.sqrt(2))
    assert square.diagonal_bd == pytest.approx(5 * math.sqrt(2))


def test_square_angles():
    square = Square(5)

    assert square.angles == pytest.approx((90, 90, 90, 90))


def test_square_is_rectangle_subclass():
    assert isinstance(Square(5), Rectangle)
    assert isinstance(Square(5), Quadrilateral)


# Parallelogram

def test_parallelogram_properties():
    parallelogram = Parallelogram(8, 5, 60)

    assert parallelogram.is_parallelogram
    assert parallelogram.classification == "parallelogram"
    assert parallelogram.area == pytest.approx(8 * 5 * math.sin(math.radians(60)))
    assert parallelogram.angles == pytest.approx((60, 120, 60, 120))


def test_parallelogram_perimeter():
    parallelogram = Parallelogram(8, 5, 60)

    assert parallelogram.perimeter == pytest.approx(26)


def test_parallelogram_invalid_angle():
    with pytest.raises(ValueError):
        Parallelogram(8, 5, 180)


# Rhombus

def test_rhombus_properties():
    rhombus = Rhombus(5, 60)

    assert rhombus.is_rhombus
    assert rhombus.is_parallelogram
    assert rhombus.classification == "rhombus"
    assert rhombus.perimeter == pytest.approx(20)
    assert rhombus.area == pytest.approx(25 * math.sin(math.radians(60)))


def test_rhombus_angles():
    rhombus = Rhombus(5, 60)

    assert rhombus.angles == pytest.approx((60, 120, 60, 120))


# Trapezoid

def test_trapezoid_properties():
    trapezoid = Trapezoid(10, 6, 4, offset=1)

    assert trapezoid.area == pytest.approx(32)
    assert trapezoid.base_a == 10
    assert trapezoid.base_c == 6
    assert trapezoid.height == 4
    assert trapezoid.offset == 1
    assert trapezoid.is_trapezoid
    assert trapezoid.classification == "trapezoid"


def test_trapezoid_perimeter():
    trapezoid = Trapezoid(10, 6, 4, offset=1)

    assert trapezoid.perimeter == pytest.approx(
        10 + 6 + math.sqrt(17) + 5
    )


def test_trapezoid_zero_offset():
    trapezoid = Trapezoid(10, 6, 4, offset=0)

    assert trapezoid.area == pytest.approx(32)
    assert trapezoid.is_trapezoid


def test_trapezoid_negative_offset():
    trapezoid = Trapezoid(10, 6, 4, offset=-1)

    assert trapezoid.area == pytest.approx(32)
    assert trapezoid.is_trapezoid


def test_trapezoid_invalid_height():
    with pytest.raises(ValueError):
        Trapezoid(10, 6, 0)


# Shared validation

@pytest.mark.parametrize(
    "factory",
    [
        lambda: Square(0),
        lambda: Rectangle(-1, 4),
        lambda: Parallelogram(8, 0, 60),
        lambda: Rhombus(5, 0),
        lambda: Trapezoid(10, 6, -2),
    ],
)
def test_invalid_dimensions(factory):
    with pytest.raises(ValueError):
        factory()


def test_string_representations():
    assert str(Square(5)) == "square"
    assert str(Rectangle(8, 4)) == "rectangle"
    assert "Square(" in repr(Square(5))
    assert "Rectangle(" in repr(Rectangle(8, 4))
