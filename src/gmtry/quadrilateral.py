
from __future__ import annotations

from math import acos, cos, degrees, isclose, isfinite, radians, sqrt
from typing import Final

__all__: Final = [
    "Quadrilateral",
    "Square",
    "Rectangle",
    "Rhombus",
    "Parallelogram",
    "Trapezoid",
]


_TOLERANCE: Final[float] = 1e-9


def _positive(value: float, name: str) -> float:
    """Validate and normalize a positive finite length."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number.")

    value = float(value)

    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite.")

    return value


def _angle(a: float, b: float, opposite: float) -> float:
    """Calculate an angle in degrees using the cosine rule."""
    if a <= 0 or b <= 0:
        raise ValueError("Triangle sides must be positive.")

    value = (a * a + b * b - opposite * opposite) / (2 * a * b)
    return degrees(acos(max(-1.0, min(1.0, value))))


def _heron(a: float, b: float, c: float) -> float:
    """Calculate a triangle's area using Heron's formula."""
    s = (a + b + c) / 2
    return sqrt(max(0.0, s * (s - a) * (s - b) * (s - c)))


def _equal(a: float, b: float) -> bool:
    return isclose(a, b, rel_tol=_TOLERANCE, abs_tol=_TOLERANCE)


class Quadrilateral:
    """A convex quadrilateral defined by four sides and diagonal AC.

    Vertices are considered in order A -> B -> C -> D.

    Args:
        a: Length of AB.
        b: Length of BC.
        c: Length of CD.
        d: Length of DA.
        diagonal_ac: Length of diagonal AC.

    A diagonal is required because four side lengths alone do not
    uniquely determine a general quadrilateral.
    """

    def __init__(
        self,
        a: float,
        b: float,
        c: float,
        d: float,
        *,
        diagonal_ac: float,
    ) -> None:
        self._side_a = _positive(a, "a")
        self._side_b = _positive(b, "b")
        self._side_c = _positive(c, "c")
        self._side_d = _positive(d, "d")
        self._diagonal_ac = _positive(diagonal_ac, "diagonal_ac")

        e = self._diagonal_ac

        # The diagonal must form two non-degenerate triangles.
        if not (
            abs(a - b) < e < a + b
            and abs(c - d) < e < c + d
        ):
            raise ValueError(
                "The given sides and diagonal cannot form "
                "a non-degenerate convex quadrilateral."
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
    def side_d(self) -> float:
        return self._side_d

    @property
    def sides(self) -> tuple[float, float, float, float]:
        return self.side_a, self.side_b, self.side_c, self.side_d

    @property
    def diagonal_ac(self) -> float:
        return self._diagonal_ac

    @property
    def perimeter(self) -> float:
        return sum(self.sides)

    @property
    def semiperimeter(self) -> float:
        return self.perimeter / 2

    @property
    def is_equilateral(self) -> bool:
        return all(_equal(self.sides[0], s) for s in self.sides[1:])

    @property
    def is_convex(self) -> bool:
        return True

    def _calculate(self) -> None:
        a, b, c, d = self.sides
        e = self.diagonal_ac

        # Split the quadrilateral along diagonal AC.
        self.area = _heron(a, b, e) + _heron(d, c, e)

        # Interior angles in vertex order A, B, C, D.
        self.angle_a = _angle(a, e, b) + _angle(d, e, c)
        self.angle_b = _angle(a, b, e)
        self.angle_c = _angle(b, e, a) + _angle(c, e, d)
        self.angle_d = _angle(d, c, e)

        self.angles = (
            self.angle_a,
            self.angle_b,
            self.angle_c,
            self.angle_d,
        )

        # Diagonal BD, calculated from the two triangles.
        x_b = (a * a + e * e - b * b) / (2 * e)
        x_d = (d * d + e * e - c * c) / (2 * e)

        y_b = sqrt(max(0.0, a * a - x_b * x_b))
        y_d = sqrt(max(0.0, d * d - x_d * x_d))

        self.diagonal_bd = sqrt(
            (x_b - x_d) ** 2 + (y_b + y_d) ** 2
        )
        self.diagonals = (self.diagonal_ac, self.diagonal_bd)

        # Side classification.
        self.is_rhombus = self.is_equilateral

        # Opposite sides parallel when consecutive interior
        # angles along a transversal sum to 180 degrees.
        self.is_parallelogram = (
            _equal(a, c)
            and _equal(b, d)
            and _equal(self.angle_a, self.angle_c)
            and _equal(self.angle_b, self.angle_d)
        )

        self.is_rectangle = all(
            _equal(angle, 90) for angle in self.angles
        )

        self.is_square = self.is_rectangle and self.is_rhombus

        # Inclusive trapezoid definition: at least one pair of
        # opposite sides is parallel, including parallelograms.
        self.is_trapezoid = (
            _equal(self.angle_a + self.angle_d, 180)
            or _equal(self.angle_b + self.angle_c, 180)
            or _equal(self.angle_a + self.angle_b, 180)
            or _equal(self.angle_c + self.angle_d, 180)
        )

        if self.is_square:
            self.classification = "square"
        elif self.is_rectangle:
            self.classification = "rectangle"
        elif self.is_rhombus:
            self.classification = "rhombus"
        elif self.is_parallelogram:
            self.classification = "parallelogram"
        elif self.is_trapezoid:
            self.classification = "trapezoid"
        else:
            self.classification = "irregular quadrilateral"

    def __str__(self) -> str:
        return self.classification

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"a={self.side_a!r}, b={self.side_b!r}, "
            f"c={self.side_c!r}, d={self.side_d!r}, "
            f"diagonal_ac={self.diagonal_ac!r})"
        )


class Rectangle(Quadrilateral):
    """A rectangle defined by its length and width."""

    def __init__(self, length: float, width: float) -> None:
        length = _positive(length, "length")
        width = _positive(width, "width")

        super().__init__(
            length,
            width,
            length,
            width,
            diagonal_ac=sqrt(length**2 + width**2),
        )

    @property
    def length(self) -> float:
        return max(self.side_a, self.side_b)

    @property
    def width(self) -> float:
        return min(self.side_a, self.side_b)


class Square(Rectangle):
    """A square defined by its side length."""

    def __init__(self, side: float) -> None:
        self._side = _positive(side, "side")
        super().__init__(self._side, self._side)

    @property
    def side(self) -> float:
        return self._side

    def __repr__(self) -> str:
        return f"Square(side={self.side!r})"


class Parallelogram(Quadrilateral):
    """A parallelogram defined by two adjacent sides and angle A."""

    def __init__(
        self,
        a: float,
        b: float,
        angle: float,
    ) -> None:
        a = _positive(a, "a")
        b = _positive(b, "b")

        if (
            isinstance(angle, bool)
            or not isinstance(angle, (int, float))
            or not isfinite(angle)
            or not 0 < angle < 180
        ):
            raise ValueError("angle must be between 0 and 180 degrees.")

        diagonal = sqrt(
            max(0.0, a * a + b * b + 2 * a * b * cos(radians(angle)))
        )

        super().__init__(
            a, b, a, b, diagonal_ac=diagonal
        )

    @property
    def angle(self) -> float:
        return self.angle_a


class Rhombus(Parallelogram):
    """A rhombus defined by its side length and angle A."""

    def __init__(self, side: float, angle: float) -> None:
        side = _positive(side, "side")
        self._side = side
        super().__init__(side, side, angle)

    @property
    def side(self) -> float:
        return self._side


class Trapezoid(Quadrilateral):
    """A trapezoid defined by its bases, height, and horizontal offset.

    The bottom base runs from (0, 0) to (base_a, 0).
    The top base runs from (offset, height) to
    (offset + base_c, height).

    Positive and negative offsets are both supported.
    """

    def __init__(
        self,
        base_a: float,
        base_c: float,
        height: float,
        *,
        offset: float = 0,
    ) -> None:
        base_a = _positive(base_a, "base_a")
        base_c = _positive(base_c, "base_c")
        height = _positive(height, "height")

        if (
            isinstance(offset, bool)
            or not isinstance(offset, (int, float))
            or not isfinite(offset)
        ):
            raise ValueError("offset must be a finite real number.")

        offset = float(offset)

        leg_b = sqrt((base_a - base_c - offset) ** 2 + height**2)
        leg_d = sqrt(offset**2 + height**2)
        diagonal_ac = sqrt((offset + base_c) ** 2 + height**2)

        super().__init__(
            base_a,
            leg_b,
            base_c,
            leg_d,
            diagonal_ac=diagonal_ac,
        )

        self.base_a = base_a
        self.base_c = base_c
        self.height = height
        self.offset = offset

    def __repr__(self) -> str:
        return (
            f"Trapezoid(base_a={self.base_a!r}, "
            f"base_c={self.base_c!r}, height={self.height!r}, "
            f"offset={self.offset!r})"
        )