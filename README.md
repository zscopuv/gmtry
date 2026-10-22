# gmtry

**A lightweight Python geometry library.**

`gmtry` provides Python classes for common geometric shapes, with calculations for area, perimeter, angles, distances, and other geometric properties. It is designed to offer a simple, consistent API for working with geometry.

## Features

- **2D geometry** — triangles, quadrilaterals, polygons, ellipses, and circles
- **Geometric properties** — areas, perimeters, angles, side lengths, and more
- **Shape classification** — identify common geometric properties and shape types
- **Input validation** — reject invalid dimensions and degenerate shapes
- **Type hints** — typed interfaces for better editor support
- **Lightweight** — built around Python's standard library

## Installation

Install from PyPI:

```bash
pip install gmtry
```

Import the classes you need:

```python
from gmtry import (
    Triangle,
    Quadrilateral,
    Rectangle,
    Square,
    Parallelogram,
    Rhombus,
    Trapezoid,
    Polygon,
    RegularPolygon,
    Ellipse,
    Circle,
)
```

## Quick start

```python
from gmtry import Circle, Rectangle, RegularPolygon, Triangle

circle = Circle(5)
print(circle.area)
print(circle.circumference)

rectangle = Rectangle(8, 4)
print(rectangle.area)
print(rectangle.perimeter)

triangle = Triangle(3, 4, 5)
print(triangle.area)
print(triangle.perimeter)

hexagon = RegularPolygon(6, 2)
print(hexagon.area)
print(hexagon.perimeter)
```

---

# API Reference

## Triangles

### `Triangle(a, b, c)`

Represents a triangle defined by its three side lengths.

| Property | Description |
|---|---|
| `a`, `b`, `c` | Side lengths |
| `area` | Triangle area |
| `perimeter` | Sum of side lengths |
| `angles` | Interior angles |
| `is_equilateral` | Whether all sides are equal |
| `is_isosceles` | Whether at least two sides are equal |
| `is_scalene` | Whether all sides differ |
| `is_right` | Whether the triangle is right-angled |
| `classification` | Triangle classification |

Example:

```python
triangle = Triangle(3, 4, 5)

print(triangle.area)
print(triangle.perimeter)
print(triangle.is_right)
```

## Quadrilaterals

### `Quadrilateral(a, b, c, d, diagonal_ac=...)`

Represents a four-sided polygon defined by its side lengths and diagonal AC.

The diagonal is required because four side lengths alone do not uniquely determine a quadrilateral.

| Property | Description |
|---|---|
| `a`, `b`, `c`, `d` | Side lengths |
| `diagonal_ac` | Length of diagonal AC |
| `area` | Quadrilateral area |
| `perimeter` | Sum of side lengths |
| `angles` | Interior angles |
| `diagonal_bd` | Length of the other diagonal |
| `is_convex` | Whether the quadrilateral is convex |
| `is_rectangle` | Whether it is a rectangle |
| `is_square` | Whether it is a square |
| `is_rhombus` | Whether all sides are equal |
| `is_parallelogram` | Whether both pairs of opposite sides are parallel |
| `is_trapezoid` | Whether at least one pair of opposite sides is parallel |

Example:

```python
shape = Quadrilateral(
    5, 4, 5, 4,
    diagonal_ac=6,
)

print(shape.area)
print(shape.perimeter)
```

### `Rectangle(length, width)`

Represents a rectangle defined by its length and width.

| Property | Description |
|---|---|
| `length` | Rectangle length |
| `width` | Rectangle width |
| `area` | Length × width |
| `perimeter` | Twice the sum of length and width |
| `diagonal_ac` | Length of the diagonal |

```python
rectangle = Rectangle(8, 4)

print(rectangle.area)       # 32
print(rectangle.perimeter)  # 24
```

### `Square(side)`

Represents a square. Inherits rectangle properties.

| Property | Description |
|---|---|
| `side` | Side length |
| `area` | Side length squared |
| `perimeter` | Four times the side length |
| `diagonal_ac` | Square diagonal |

```python
square = Square(5)

print(square.area)       # 25
print(square.perimeter)  # 20
```

### `Parallelogram(a, b, angle)`

Represents a parallelogram defined by two adjacent side lengths and their included angle.

| Property | Description |
|---|---|
| `a`, `b` | Adjacent side lengths |
| `angle` | Included angle |
| `area` | Area calculated from the sides and angle |
| `perimeter` | Twice the sum of adjacent side lengths |

```python
parallelogram = Parallelogram(6, 4, 60)

print(parallelogram.area)
print(parallelogram.perimeter)
```

### `Rhombus(side, angle)`

Represents a rhombus defined by its side length and included angle. Inherits parallelogram properties.

| Property | Description |
|---|---|
| `side` | Side length |
| `angle` | Included angle |
| `area` | Area calculated from the side and angle |
| `perimeter` | Four times the side length |

```python
rhombus = Rhombus(5, 60)

print(rhombus.area)
print(rhombus.perimeter)
```

### `Trapezoid(base_a, base_c, height, offset=0)`

Represents a trapezoid using its parallel base lengths, height, and horizontal offset.

| Parameter | Description |
|---|---|
| `base_a` | First base length |
| `base_c` | Second base length |
| `height` | Perpendicular distance between the bases |
| `offset` | Horizontal offset between the base endpoints |

| Property | Description |
|---|---|
| `area` | Area calculated from both bases and height |
| `perimeter` | Sum of all four side lengths |

```python
trapezoid = Trapezoid(10, 6, 4, offset=1)

print(trapezoid.area)
print(trapezoid.perimeter)
```

## Polygons

### `Polygon(vertices)`

Represents a simple polygon defined by an ordered sequence of 2D vertices.

Vertices must follow the polygon boundary in either clockwise or counterclockwise order. Self-intersecting and degenerate polygons are rejected.

| Property / method | Description |
|---|---|
| `vertices` | Ordered vertex coordinates |
| `n` | Number of vertices and sides |
| `sides` | Side lengths |
| `side_lengths` | Alias for `sides` |
| `area` | Absolute polygon area |
| `signed_area` | Signed area indicating vertex orientation |
| `perimeter` | Sum of side lengths |
| `angles` | Interior angles in radians |
| `interior_angles` | Interior angles in radians |
| `is_convex` | Whether the polygon is convex |
| `is_regular` | Whether the polygon is regular |
| `contains_point(x, y)` | Whether a point lies inside or on the boundary |

```python
polygon = Polygon([
    (0, 0),
    (4, 0),
    (3, 2),
    (0, 2),
])

print(polygon.area)
print(polygon.perimeter)
print(polygon.is_convex)
print(polygon.contains_point(1, 1))
```

**Note:** Polygon angles are expressed in radians.

### `RegularPolygon(n, side_length, center=(0, 0), rotation=0)`

Represents a regular polygon with equal side lengths and equal interior angles. Inherits from `Polygon`.

| Parameter | Description |
|---|---|
| `n` | Number of sides; must be at least 3 |
| `side_length` | Length of each side |
| `center` | Center coordinates |
| `rotation` | Rotation in radians |

| Property | Description |
|---|---|
| `side_length` | Length of each side |
| `center` | Center coordinates |
| `rotation` | Rotation angle in radians |
| `circumradius` | Distance from the center to a vertex |
| `inradius` | Distance from the center to a side |
| `apothem` | Alias for the inradius |
| `interior_angle` | One interior angle in radians |
| `exterior_angle` | One exterior angle in radians |
| `area` | Regular polygon area |
| `perimeter` | Number of sides × side length |

```python
hexagon = RegularPolygon(6, 2)

print(hexagon.area)
print(hexagon.perimeter)
print(hexagon.circumradius)
print(hexagon.inradius)
```

## Ellipses and circles

### `Ellipse(a, b)`

Represents an ellipse centered at the origin, defined by its two semi-axis lengths. The larger semi-axis is designated the major axis and aligned with the x-axis.

| Property / method | Description |
|---|---|
| `a` | Semi-major axis |
| `b` | Semi-minor axis |
| `semi_major_axis` | Semi-major axis length |
| `semi_minor_axis` | Semi-minor axis length |
| `major_axis` | Full major axis length |
| `minor_axis` | Full minor axis length |
| `area` | Ellipse area |
| `circumference` | Approximate circumference using Ramanujan's formula |
| `focal_distance` | Distance from the center to either focus |
| `foci` | Coordinates of the two foci |
| `eccentricity` | Measure of deviation from a circle |
| `is_circle` | Whether the axes are equal |
| `classification` | `"circle"` or `"ellipse"` |
| `contains_point(x, y)` | Whether a point lies inside or on the boundary |

```python
ellipse = Ellipse(5, 3)

print(ellipse.area)
print(ellipse.circumference)
print(ellipse.eccentricity)
print(ellipse.foci)
```

### `Circle(radius)`

Represents a circle. Inherits ellipse properties.

| Property | Description |
|---|---|
| `radius` | Circle radius |
| `diameter` | Twice the radius |
| `area` | π × radius² |
| `circumference` | 2 × π × radius |
| `is_unit_circle` | Whether the radius is approximately 1 |
| `eccentricity` | Zero |
| `foci` | Two coincident foci at the origin |

```python
circle = Circle(5)

print(circle.area)
print(circle.circumference)
print(circle.diameter)
print(circle.is_unit_circle)
```

---

## Validation and numerical conventions

- Dimensions must be positive and finite where applicable.
- Invalid geometric configurations raise exceptions rather than silently producing invalid shapes.
- Polygon coordinates are represented as `(x, y)` tuples.
- Polygon angles and rotation values use radians.
- Floating-point calculations can introduce small numerical differences.
- Ellipse circumference is an approximation, not an exact closed-form calculation.

## Development

Clone the repository and install the project in editable mode:

```bash
git clone https://github.com/zscopuv/gmtry.git
cd gmtry
python -m pip install -e .
```

Install the testing dependency and run the test suite:

```bash
python -m pip install pytest
python -m pytest -v
```

## Project status

`gmtry` is under active development. The API and available shape classes may evolve between releases.

## License

See the repository's `LICENSE` file for licensing terms.