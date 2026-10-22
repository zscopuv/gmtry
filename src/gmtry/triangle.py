
from __future__ import annotations

from math import acos, isclose, isfinite, sqrt, pi
from typing import Final

__all__: Final = ["Triangle"]


class Triangle:
    """Represent a valid triangle and calculate its geometric properties.

    All lengths use the same arbitrary unit. Angles are expressed in degrees.

    Raises:
        TypeError: If a side is not a real number.
        ValueError: If a side is non-positive, non-finite, or the sides
            cannot form a non-degenerate triangle.
    """

    _TOLERANCE: Final[float] = 1e-9

    def __init__(self, a: float, b: float, c: float) -> None:
        sides = (a, b, c)

        for side in sides:
            if isinstance(side, bool) or not isinstance(side, (int, float)):
                raise TypeError("Triangle sides must be real numbers.")

            if not isfinite(side):
                raise ValueError("Triangle sides must be finite.")

            if side <= 0:
                raise ValueError("Triangle sides must be positive.")

        self._side_a = float(a)
        self._side_b = float(b)
        self._side_c = float(c)

        x, y, z = sorted(sides)

        if x + y <= z:
            raise ValueError(
                "The sum of any two sides must exceed the third side."
            )

        self._calculate()

    @property
    def side_a(self) -> float:
        return self._side_a

    @property
    def side_b(self) -> float:
        return self._side_b

    @property
    def side_c(self) -> float:
        return self._side_c

    @property
    def sides(self) -> tuple[float, float, float]:
        return self.side_a, self.side_b, self.side_c

    @property
    def classification(self) -> str:
        return f"{self.angle_classification} {self.side_classification} triangle"

    def __str__(self) -> str:
        return self.classification

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"a={self.side_a!r}, b={self.side_b!r}, c={self.side_c!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Triangle):
            return NotImplemented

        return sorted(self.sides) == sorted(other.sides)

    def _calculate(self) -> None:
        a, b, c = self.sides
        tolerance = self._TOLERANCE

        # Basic measurements
        self.perimeter = a + b + c
        self.semiperimeter = self.perimeter / 2

        # Heron's formula
        s = self.semiperimeter
        self.area = sqrt(s * (s - a) * (s - b) * (s - c))

        # Side classification
        self.is_equilateral = (
            isclose(a, b, rel_tol=tolerance)
            and isclose(b, c, rel_tol=tolerance)
        )

        self.is_isosceles = (
            self.is_equilateral
            or isclose(a, b, rel_tol=tolerance)
            or isclose(b, c, rel_tol=tolerance)
            or isclose(a, c, rel_tol=tolerance)
        )

        self.is_scalene = not self.is_isosceles

        if self.is_equilateral:
            self.side_classification = "equilateral"
        elif self.is_isosceles:
            self.side_classification = "isosceles"
        else:
            self.side_classification = "scalene"

        # Angle classification, based on the Pythagorean theorem
        x, y, z = sorted(self.sides)
        lhs = x * x + y * y
        rhs = z * z

        self.is_right = isclose(
            lhs, rhs, rel_tol=tolerance, abs_tol=tolerance
        )
        self.is_acute = lhs > rhs and not self.is_right
        self.is_obtuse = lhs < rhs and not self.is_right

        if self.is_right:
            self.angle_classification = "right"
        elif self.is_obtuse:
            self.angle_classification = "obtuse"
        else:
            self.angle_classification = "acute"

        # Angles opposite sides a, b and c
        def angle(opposite: float, side1: float, side2: float) -> float:
            cosine = (
                side1**2 + side2**2 - opposite**2
            ) / (2 * side1 * side2)

            # Protect acos from floating-point rounding errors.
            cosine = max(-1.0, min(1.0, cosine))
            return acos(cosine) * 180 / pi

        self.angle_a = angle(a, b, c)
        self.angle_b = angle(b, a, c)
        self.angle_c = angle(c, a, b)
        self.angles = (self.angle_a, self.angle_b, self.angle_c)

        # Inscribed and circumscribed circles
        self.inradius = self.area / s
        self.circumradius = (a * b * c) / (4 * self.area)

        # Altitudes (heights)
        self.height_a = 2 * self.area / a
        self.height_b = 2 * self.area / b
        self.height_c = 2 * self.area / c

    def is_congruent_to(self, other: Triangle) -> bool:
        """Return whether two triangles have the same side lengths."""
        return self == other