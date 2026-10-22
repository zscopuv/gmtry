
from __future__ import annotations

from math import isclose, isfinite, pi, sqrt
from typing import Final

__all__: Final = ["Ellipse", "Circle"]

_TOLERANCE: Final[float] = 1e-9


def _positive(value: float, name: str) -> float:
    """Validate and normalize a positive finite number."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number.")

    value = float(value)

    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite.")

    return value


class Ellipse:
    """Represent an ellipse centered at the origin.

    Args:
        a: Length of the first semi-axis.
        b: Length of the second semi-axis.

    The larger semi-axis is treated as the major axis, oriented along
    the x-axis. The smaller semi-axis is oriented along the y-axis.

    Circumference is approximated using Ramanujan's second formula.
    """

    def __init__(self, a: float, b: float) -> None:
        a = _positive(a, "a")
        b = _positive(b, "b")

        self._semi_major_axis = max(a, b)
        self._semi_minor_axis = min(a, b)

        self._calculate()

    @property
    def semi_major_axis(self) -> float:
        return self._semi_major_axis

    @property
    def semi_minor_axis(self) -> float:
        return self._semi_minor_axis

    @property
    def major_axis(self) -> float:
        """Full length of the major axis."""
        return 2 * self.semi_major_axis

    @property
    def minor_axis(self) -> float:
        """Full length of the minor axis."""
        return 2 * self.semi_minor_axis

    @property
    def a(self) -> float:
        """Alias for the semi-major axis."""
        return self.semi_major_axis

    @property
    def b(self) -> float:
        """Alias for the semi-minor axis."""
        return self.semi_minor_axis

    @property
    def is_circle(self) -> bool:
        return isclose(
            self.a,
            self.b,
            rel_tol=_TOLERANCE,
            abs_tol=_TOLERANCE,
        )

    @property
    def classification(self) -> str:
        return "circle" if self.is_circle else "ellipse"

    def _calculate(self) -> None:
        a = self.semi_major_axis
        b = self.semi_minor_axis

        self.area = pi * a * b

        # Ramanujan's second approximation of the circumference.
        h = ((a - b) / (a + b)) ** 2

        self.circumference = (
            pi * (a + b)
            * (1 + (3 * h) / (10 + sqrt(4 - 3 * h)))
        )

        # Linear eccentricity: distance from center to either focus.
        self.focal_distance = sqrt(max(0.0, a * a - b * b))

        # Foci are symmetric around the origin on the major axis.
        c = self.focal_distance
        self.foci = ((-c, 0.0), (c, 0.0))

        # Eccentricity ranges from 0 (circle) toward 1.
        self.eccentricity = c / a

    def contains_point(self, x: float, y: float) -> bool:
        """Return whether point (x, y) lies inside or on the ellipse."""
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError("x must be a real number.")

        if isinstance(y, bool) or not isinstance(y, (int, float)):
            raise TypeError("y must be a real number.")

        if not isfinite(x) or not isfinite(y):
            raise ValueError("Coordinates must be finite.")

        a = self.semi_major_axis
        b = self.semi_minor_axis

        return (x / a) ** 2 + (y / b) ** 2 <= 1 + _TOLERANCE

    def __str__(self) -> str:
        return self.classification

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"a={self.semi_major_axis!r}, "
            f"b={self.semi_minor_axis!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ellipse):
            return NotImplemented

        return (
            self.semi_major_axis == other.semi_major_axis
            and self.semi_minor_axis == other.semi_minor_axis
        )


class Circle(Ellipse):
    """Represent a circle, a special case of an ellipse.

    Args:
        radius: Circle radius.
    """

    def __init__(self, radius: float) -> None:
        self._radius = _positive(radius, "radius")
        super().__init__(self._radius, self._radius)

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def diameter(self) -> float:
        return 2 * self.radius

    @property
    def is_unit_circle(self) -> bool:
        return isclose(
            self.radius,
            1.0,
            rel_tol=_TOLERANCE,
            abs_tol=_TOLERANCE,
        )

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius!r})"
