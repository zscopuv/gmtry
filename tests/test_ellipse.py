
import math

import pytest

from gmtry import Circle, Ellipse


# Ellipse basics

def test_ellipse_area():
    ellipse = Ellipse(5, 3)

    assert ellipse.area == pytest.approx(15 * math.pi)


def test_ellipse_circumference():
    ellipse = Ellipse(5, 3)

    h = ((5 - 3) / (5 + 3)) ** 2
    expected = math.pi * (5 + 3) * (
        1 + (3 * h) / (10 + math.sqrt(4 - 3 * h))
    )

    assert ellipse.circumference == pytest.approx(expected)


def test_ellipse_axes():
    ellipse = Ellipse(5, 3)

    assert ellipse.semi_major_axis == 5
    assert ellipse.semi_minor_axis == 3
    assert ellipse.major_axis == 10
    assert ellipse.minor_axis == 6
    assert ellipse.a == 5
    assert ellipse.b == 3


def test_ellipse_normalizes_axes():
    ellipse = Ellipse(3, 5)

    assert ellipse.a == 5
    assert ellipse.b == 3


def test_ellipse_eccentricity():
    ellipse = Ellipse(5, 3)

    assert ellipse.focal_distance == pytest.approx(4)
    assert ellipse.eccentricity == pytest.approx(0.8)


def test_ellipse_foci():
    ellipse = Ellipse(5, 3)

    assert ellipse.foci[0] == pytest.approx((-4, 0))
    assert ellipse.foci[1] == pytest.approx((4, 0))

def test_ellipse_classification():
    assert str(Ellipse(5, 3)) == "ellipse"
    assert Ellipse(5, 3).classification == "ellipse"
    assert not Ellipse(5, 3).is_circle


# Circle

def test_circle_area():
    circle = Circle(5)

    assert circle.area == pytest.approx(25 * math.pi)


def test_circle_circumference():
    circle = Circle(5)

    assert circle.circumference == pytest.approx(10 * math.pi)


def test_circle_radius_and_diameter():
    circle = Circle(5)

    assert circle.radius == 5
    assert circle.diameter == 10
    assert circle.semi_major_axis == 5
    assert circle.semi_minor_axis == 5


def test_circle_is_unit_circle():
    assert Circle(1).is_unit_circle
    assert not Circle(5).is_unit_circle


def test_circle_has_zero_eccentricity():
    circle = Circle(5)

    assert circle.eccentricity == pytest.approx(0)
    assert circle.focal_distance == pytest.approx(0)
    assert circle.foci[0] == pytest.approx((0, 0))
    assert circle.foci[1] == pytest.approx((0, 0))

def test_circle_inherits_from_ellipse():
    circle = Circle(5)

    assert isinstance(circle, Ellipse)
    assert circle.is_circle
    assert circle.classification == "circle"
    assert str(circle) == "circle"


# Point containment

@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        (0, 0, True),
        (5, 0, True),
        (-5, 0, True),
        (0, 3, True),
        (2, 1, True),
        (6, 0, False),
        (0, 4, False),
        (5, 3, False),
    ],
)
def test_ellipse_contains_point(x, y, expected):
    assert Ellipse(5, 3).contains_point(x, y) is expected


def test_circle_contains_point():
    circle = Circle(5)

    assert circle.contains_point(3, 4)
    assert circle.contains_point(0, 0)
    assert not circle.contains_point(4, 4)


# Equality and representations

def test_ellipse_equality():
    assert Ellipse(5, 3) == Ellipse(3, 5)
    assert Ellipse(5, 3) != Ellipse(5, 2)


def test_circle_equality():
    assert Circle(5) == Circle(5)
    assert Circle(5) != Circle(3)


def test_ellipse_repr():
    assert repr(Ellipse(5, 3)) == "Ellipse(a=5.0, b=3.0)"


def test_circle_repr():
    assert repr(Circle(5)) == "Circle(radius=5.0)"


# Input validation

@pytest.mark.parametrize(
    ("a", "b"),
    [
        (0, 3),
        (5, 0),
        (-1, 3),
        (5, -1),
        (math.inf, 3),
        (5, math.nan),
    ],
)
def test_ellipse_rejects_invalid_axes(a, b):
    with pytest.raises(ValueError):
        Ellipse(a, b)


@pytest.mark.parametrize("radius", [0, -1, math.inf, math.nan])
def test_circle_rejects_invalid_radius(radius):
    with pytest.raises(ValueError):
        Circle(radius)


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("5", 3),
        (5, "3"),
        (True, 3),
        (5, False),
    ],
)
def test_ellipse_rejects_invalid_types(a, b):
    with pytest.raises(TypeError):
        Ellipse(a, b)


def test_circle_rejects_boolean_radius():
    with pytest.raises(TypeError):
        Circle(True)


@pytest.mark.parametrize(
    ("x", "y"),
    [
        ("1", 2),
        (1, "2"),
        (True, 2),
        (1, False),
    ],
)
def test_contains_point_rejects_invalid_types(x, y):
    with pytest.raises(TypeError):
        Ellipse(5, 3).contains_point(x, y)


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (math.inf, 0),
        (0, math.nan),
    ],
)
def test_contains_point_rejects_non_finite_coordinates(x, y):
    with pytest.raises(ValueError):
        Ellipse(5, 3).contains_point(x, y)
