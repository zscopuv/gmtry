
from __future__ import annotations

from math import acos, atan2, cos, hypot, isfinite, pi, sin, sqrt
from typing import Final, Sequence

__all__: Final = ["Polygon", "RegularPolygon"]

_TOLERANCE: Final[float] = 1e-9
Point = tuple[float, float]


def _number(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number.")

    value = float(value)

    if not isfinite(value):
        raise ValueError(f"{name} must be finite.")

    return value


def _positive(value: float, name: str) -> float:
    value = _number(value, name)

    if value <= 0:
        raise ValueError(f"{name} must be positive.")

    return value


def _point(value: Sequence[float], name: str) -> Point:
    if isinstance(value, (str, bytes)) or len(value) != 2:
        raise ValueError(f"{name} must contain exactly two coordinates.")

    return (
        _number(value[0], f"{name}[0]"),
        _number(value[1], f"{name}[1]"),
    )


def _cross(a: Point, b: Point, c: Point) -> float:
    """Signed cross product of AB and AC."""
    return (
        (b[0] - a[0]) * (c[1] - a[1])
        - (b[1] - a[1]) * (c[0] - a[0])
    )


def _distance(a: Point, b: Point) -> float:
    return hypot(b[0] - a[0], b[1] - a[1])


def _on_segment(a: Point, b: Point, p: Point) -> bool:
    return (
        min(a[0], b[0]) - _TOLERANCE
        <= p[0]
        <= max(a[0], b[0]) + _TOLERANCE
        and min(a[1], b[1]) - _TOLERANCE
        <= p[1]
        <= max(a[1], b[1]) + _TOLERANCE
        and abs(_cross(a, b, p)) <= _TOLERANCE
    )


def _segments_intersect(
    a: Point,
    b: Point,
    c: Point,
    d: Point,
) -> bool:
    ab_c = _cross(a, b, c)
    ab_d = _cross(a, b, d)
    cd_a = _cross(c, d, a)
    cd_b = _cross(c, d, b)

    if (
        ((ab_c > _TOLERANCE and ab_d < -_TOLERANCE)
         or (ab_c < -_TOLERANCE and ab_d > _TOLERANCE))
        and
        ((cd_a > _TOLERANCE and cd_b < -_TOLERANCE)
         or (cd_a < -_TOLERANCE and cd_b > _TOLERANCE))
    ):
        return True

    return (
        (abs(ab_c) <= _TOLERANCE and _on_segment(a, b, c))
        or (abs(ab_d) <= _TOLERANCE and _on_segment(a, b, d))
        or (abs(cd_a) <= _TOLERANCE and _on_segment(c, d, a))
        or (abs(cd_b) <= _TOLERANCE and _on_segment(c, d, b))
    )


class Polygon:
    """Represent a simple polygon defined by ordered 2D vertices.

    Vertices must be supplied in boundary order, either clockwise
    or counterclockwise. The polygon must be non-degenerate and
    cannot have intersecting non-adjacent edges.
    """

    def __init__(self, vertices: Sequence[Sequence[float]]) -> None:
        if isinstance(vertices, (str, bytes)):
            raise TypeError("vertices must be a sequence of 2D points.")

        try:
            points = tuple(
                _point(vertex, f"vertices[{i}]")
                for i, vertex in enumerate(vertices)
            )
        except TypeError:
            raise TypeError(
                "vertices must be an iterable of 2D points."
            ) from None

        if len(points) < 3:
            raise ValueError("A polygon requires at least three vertices.")

        if len(set(points)) != len(points):
            raise ValueError("Polygon vertices must be distinct.")

        for i, point in enumerate(points):
            following = points[(i + 1) % len(points)]

            if _distance(point, following) <= _TOLERANCE:
                raise ValueError("Consecutive vertices must be distinct.")

        self._vertices = points
        self._calculate()

    @property
    def vertices(self) -> tuple[Point, ...]:
        return self._vertices

    @property
    def n(self) -> int:
        """Number of vertices (and sides)."""
        return len(self.vertices)

    @property
    def sides(self) -> tuple[float, ...]:
        return tuple(
            _distance(self.vertices[i], self.vertices[(i + 1) % self.n])
            for i in range(self.n)
        )

    @property
    def side_lengths(self) -> tuple[float, ...]:
        return self.sides

    @property
    def interior_angles(self) -> tuple[float, ...]:
        return self._interior_angles

    @property
    def angles(self) -> tuple[float, ...]:
        return self.interior_angles

    @property
    def perimeter(self) -> float:
        return sum(self.sides)

    @property
    def area(self) -> float:
        return abs(self.signed_area)

    @property
    def signed_area(self) -> float:
        """Signed area: positive for CCW vertex order."""
        total = 0.0

        for i, (x1, y1) in enumerate(self.vertices):
            x2, y2 = self.vertices[(i + 1) % self.n]
            total += x1 * y2 - x2 * y1

        return total / 2.0

    @property
    def is_convex(self) -> bool:
        signs = []

        for i in range(self.n):
            a = self.vertices[i - 1]
            b = self.vertices[i]
            c = self.vertices[(i + 1) % self.n]
            turn = _cross(a, b, c)

            if abs(turn) > _TOLERANCE:
                signs.append(turn > 0)

        return bool(signs) and all(sign == signs[0] for sign in signs)

    @property
    def is_regular(self) -> bool:
        sides = self.sides
        angles = self.interior_angles

        return (
            self.is_convex
            and all(
                abs(side - sides[0]) <= _TOLERANCE
                for side in sides[1:]
            )
            and all(
                abs(angle - angles[0]) <= _TOLERANCE
                for angle in angles[1:]
            )
        )

    def contains_point(self, x: float, y: float) -> bool:
        """Return True if a point lies inside or on the boundary."""
        point = (
            _number(x, "x"),
            _number(y, "y"),
        )

        inside = False
        px, py = point

        for i, (x1, y1) in enumerate(self.vertices):
            x2, y2 = self.vertices[(i + 1) % self.n]

            if _on_segment((x1, y1), (x2, y2), point):
                return True

            if (y1 > py) != (y2 > py):
                intersection_x = (
                    x1 + (py - y1) * (x2 - x1) / (y2 - y1)
                )

                if px < intersection_x:
                    inside = not inside

        return inside

    def _calculate(self) -> None:
        points = self.vertices

        # Reject intersecting non-adjacent edges.
        for i in range(self.n):
            a = points[i]
            b = points[(i + 1) % self.n]

            for j in range(i + 1, self.n):
                # Adjacent edges share an endpoint by design.
                if j == i or j == (i + 1) % self.n:
                    continue
                if i == (j + 1) % self.n:
                    continue

                c = points[j]
                d = points[(j + 1) % self.n]

                if _segments_intersect(a, b, c, d):
                    raise ValueError(
                        "Polygon edges must not intersect."
                    )

        signed_area = self.signed_area

        if abs(signed_area) <= _TOLERANCE:
            raise ValueError("Polygon area must be non-zero.")

        orientation = 1.0 if signed_area > 0 else -1.0
        angles = []

        for i in range(self.n):
            previous = points[i - 1]
            current = points[i]
            following = points[(i + 1) % self.n]

            incoming = (
                current[0] - previous[0],
                current[1] - previous[1],
            )
            outgoing = (
                following[0] - current[0],
                following[1] - current[1],
            )

            turn = atan2(
                incoming[0] * outgoing[1]
                - incoming[1] * outgoing[0],
                incoming[0] * outgoing[0]
                + incoming[1] * outgoing[1],
            )

            angles.append(pi - orientation * turn)

        self._interior_angles = tuple(angles)

    def __str__(self) -> str:
        return type(self).__name__

    def __repr__(self) -> str:
        return f"{type(self).__name__}(vertices={self.vertices!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polygon):
            return NotImplemented

        return (
            self.n == other.n
            and self.area == other.area
            and self.perimeter == other.perimeter
            and self.vertices == other.vertices
        )


class RegularPolygon(Polygon):
    """Create a regular polygon from its side count and side length.

    Args:
        n: Number of sides, at least 3.
        side_length: Length of each side.
        center: Coordinates of the center.
        rotation: Rotation in radians, counterclockwise from the
            positive x-axis to the first vertex.
    """

    def __init__(
        self,
        n: int,
        side_length: float,
        *,
        center: Sequence[float] = (0.0, 0.0),
        rotation: float = 0.0,
    ) -> None:
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("n must be an integer.")

        if n < 3:
            raise ValueError("A regular polygon requires at least 3 sides.")

        side_length = _positive(side_length, "side_length")
        center_x, center_y = _point(center, "center")
        rotation = _number(rotation, "rotation")

        circumradius = side_length / (2.0 * sin(pi / n))

        vertices = tuple(
            (
                center_x + circumradius * cos(rotation + 2 * pi * i / n),
                center_y + circumradius * sin(rotation + 2 * pi * i / n),
            )
            for i in range(n)
        )

        self._side_count = n
        self._side_length = side_length
        self._center = (center_x, center_y)
        self._rotation = rotation

        super().__init__(vertices)

    @property
    def n(self) -> int:
        return self._side_count

    @property
    def side_length(self) -> float:
        return self._side_length

    @property
    def center(self) -> Point:
        return self._center

    @property
    def rotation(self) -> float:
        return self._rotation

    @property
    def circumradius(self) -> float:
        return self.side_length / (2.0 * sin(pi / self.n))

    @property
    def inradius(self) -> float:
        return self.side_length / (2.0 * __import__("math").tan(pi / self.n))

    @property
    def apothem(self) -> float:
        return self.inradius

    @property
    def interior_angle(self) -> float:
        return (self.n - 2) * pi / self.n

    @property
    def exterior_angle(self) -> float:
        return 2 * pi / self.n

    @property
    def perimeter(self) -> float:
        return self.n * self.side_length

    @property
    def area(self) -> float:
        return (
            self.n
            * self.side_length**2
            / (4.0 * __import__("math").tan(pi / self.n))
        )

    def __repr__(self) -> str:
        return (
            f"RegularPolygon(n={self.n}, "
            f"side_length={self.side_length!r}, "
            f"center={self.center!r}, rotation={self.rotation!r})"
        )
