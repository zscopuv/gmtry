
import math

import pytest

from gmtry import Polygon, RegularPolygon


# Polygon basics


def test_triangle_area_and_perimeter():
    polygon = Polygon([(0, 0), (4, 0), (0, 3)])

    assert polygon.area == pytest.approx(6)
    assert polygon.perimeter == pytest.approx(12)
    assert polygon.n == 3


def test_square_area_and_perimeter():
    polygon = Polygon([
        (0, 0),
        (2, 0),
        (2, 2),
        (0, 2),
    ])

    assert polygon.area == pytest.approx(4)
    assert polygon.perimeter == pytest.approx(8)
    assert polygon.n == 4


def test_rectangle_area_and_perimeter():
    polygon = Polygon([
        (0, 0),
        (5, 0),
        (5, 3),
        (0, 3),
    ])

    assert polygon.area == pytest.approx(15)
    assert polygon.perimeter == pytest.approx(16)


def test_side_lengths():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (4, 3),
        (0, 3),
    ])

    assert polygon.sides == pytest.approx((4, 3, 4, 3))
    assert polygon.side_lengths == pytest.approx((4, 3, 4, 3))


def test_vertices_are_immutable_tuple():
    polygon = Polygon([(0, 0), (4, 0), (0, 3)])

    assert isinstance(polygon.vertices, tuple)
    assert polygon.vertices == ((0.0, 0.0), (4.0, 0.0), (0.0, 3.0))


def test_repr_and_str():
    polygon = Polygon([(0, 0), (4, 0), (0, 3)])

    assert str(polygon) == "Polygon"
    assert "Polygon(vertices=" in repr(polygon)


# Area orientation


def test_counterclockwise_signed_area():
    polygon = Polygon([(0, 0), (4, 0), (4, 3), (0, 3)])

    assert polygon.signed_area == pytest.approx(12)
    assert polygon.area == pytest.approx(12)


def test_clockwise_signed_area():
    polygon = Polygon([(0, 0), (0, 3), (4, 3), (4, 0)])

    assert polygon.signed_area == pytest.approx(-12)
    assert polygon.area == pytest.approx(12)


def test_reversed_vertices_preserve_area_and_perimeter():
    vertices = [(0, 0), (4, 0), (4, 3), (0, 3)]

    first = Polygon(vertices)
    second = Polygon(list(reversed(vertices)))

    assert second.area == pytest.approx(first.area)
    assert second.perimeter == pytest.approx(first.perimeter)


# Angles


def test_square_interior_angles():
    polygon = Polygon([
        (0, 0),
        (2, 0),
        (2, 2),
        (0, 2),
    ])

    assert polygon.interior_angles == pytest.approx(
        (math.pi / 2,) * 4
    )
    assert polygon.angles == pytest.approx(
        (math.pi / 2,) * 4
    )


def test_triangle_interior_angle_sum():
    polygon = Polygon([(0, 0), (4, 0), (0, 3)])

    assert sum(polygon.interior_angles) == pytest.approx(math.pi)


def test_quadrilateral_interior_angle_sum():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (4, 3),
        (0, 3),
    ])

    assert sum(polygon.interior_angles) == pytest.approx(2 * math.pi)


def test_concave_polygon_interior_angle_sum():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (2, 1),
        (4, 4),
        (0, 4),
    ])

    assert sum(polygon.interior_angles) == pytest.approx(3 * math.pi)
    assert any(angle > math.pi for angle in polygon.interior_angles)


# Convexity and regularity


def test_square_is_convex():
    polygon = Polygon([
        (0, 0),
        (2, 0),
        (2, 2),
        (0, 2),
    ])

    assert polygon.is_convex is True


def test_concave_polygon_is_not_convex():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (2, 1),
        (4, 4),
        (0, 4),
    ])

    assert polygon.is_convex is False


def test_square_is_regular():
    polygon = Polygon([
        (0, 0),
        (2, 0),
        (2, 2),
        (0, 2),
    ])

    assert polygon.is_regular is True


def test_rectangle_is_not_regular():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (4, 2),
        (0, 2),
    ])

    assert polygon.is_regular is False


def test_equilateral_triangle_is_regular():
    height = math.sqrt(3) / 2

    polygon = Polygon([
        (0, 0),
        (1, 0),
        (0.5, height),
    ])

    assert polygon.is_regular is True


# Point containment


def test_point_inside_polygon():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (4, 4),
        (0, 4),
    ])

    assert polygon.contains_point(2, 2) is True


def test_point_outside_polygon():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (4, 4),
        (0, 4),
    ])

    assert polygon.contains_point(5, 2) is False


def test_point_on_edge_counts_as_contained():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (4, 4),
        (0, 4),
    ])

    assert polygon.contains_point(2, 0) is True


def test_point_on_vertex_counts_as_contained():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (4, 4),
        (0, 4),
    ])

    assert polygon.contains_point(0, 0) is True


def test_point_containment_for_concave_polygon():
    polygon = Polygon([
        (0, 0),
        (4, 0),
        (2, 1),
        (4, 4),
        (0, 4),
    ])

    assert polygon.contains_point(1, 2) is True
    assert polygon.contains_point(3, 2) is False


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (True, 0),
        (0, False),
        ("1", 0),
        (0, "1"),
    ],
)
def test_contains_point_rejects_invalid_coordinates(x, y):
    polygon = Polygon([(0, 0), (4, 0), (0, 3)])

    with pytest.raises(TypeError):
        polygon.contains_point(x, y)


@pytest.mark.parametrize(
    ("x", "y"),
    [
        (math.inf, 0),
        (0, -math.inf),
        (math.nan, 0),
    ],
)
def test_contains_point_rejects_nonfinite_coordinates(x, y):
    polygon = Polygon([(0, 0), (4, 0), (0, 3)])

    with pytest.raises(ValueError):
        polygon.contains_point(x, y)


# Validation


def test_rejects_too_few_vertices():
    with pytest.raises(ValueError):
        Polygon([(0, 0), (1, 1)])


def test_rejects_duplicate_vertices():
    with pytest.raises(ValueError):
        Polygon([(0, 0), (4, 0), (0, 3), (4, 0)])


def test_rejects_repeated_closing_vertex():
    with pytest.raises(ValueError):
        Polygon([(0, 0), (4, 0), (0, 3), (0, 0)])


def test_rejects_consecutive_duplicate_vertices():
    with pytest.raises(ValueError):
        Polygon([(0, 0), (4, 0), (4, 0), (0, 3)])


def test_rejects_invalid_point_dimensions():
    with pytest.raises(ValueError):
        Polygon([(0, 0), (1, 1), (2, 2, 2)])


def test_rejects_string_as_vertices():
    with pytest.raises(TypeError):
        Polygon("invalid")


def test_rejects_boolean_coordinate():
    with pytest.raises(TypeError):
        Polygon([(False, 0), (1, 0), (0, 1)])


def test_rejects_nonfinite_vertex():
    with pytest.raises(ValueError):
        Polygon([(0, 0), (math.inf, 0), (0, 1)])


def test_rejects_collinear_vertices():
    with pytest.raises(ValueError):
        Polygon([(0, 0), (1, 0), (2, 0)])


def test_rejects_self_intersecting_bowtie():
    with pytest.raises(ValueError):
        Polygon([
            (0, 0),
            (2, 2),
            (0, 2),
            (2, 0),
        ])


def test_rejects_self_intersecting_polygon():
    with pytest.raises(ValueError):
        Polygon([
            (0, 0),
            (4, 0),
            (0, 4),
            (4, 4),
            (2, -1),
        ])


# Equality


def test_equal_polygons():
    first = Polygon([(0, 0), (4, 0), (0, 3)])
    second = Polygon([(0, 0), (4, 0), (0, 3)])

    assert first == second


def test_different_polygons_are_not_equal():
    first = Polygon([(0, 0), (4, 0), (0, 3)])
    second = Polygon([(0, 0), (5, 0), (0, 3)])

    assert first != second


def test_polygon_is_not_equal_to_unrelated_object():
    polygon = Polygon([(0, 0), (4, 0), (0, 3)])

    assert polygon != "polygon"


# RegularPolygon


def test_regular_polygon_triangle():
    triangle = RegularPolygon(3, 2)

    assert triangle.n == 3
    assert triangle.side_length == pytest.approx(2)
    assert triangle.perimeter == pytest.approx(6)
    assert triangle.area == pytest.approx(math.sqrt(3))
    assert triangle.is_regular is True


def test_regular_polygon_square():
    square = RegularPolygon(4, 2)

    assert square.n == 4
    assert square.perimeter == pytest.approx(8)
    assert square.area == pytest.approx(4)
    assert square.is_regular is True


def test_regular_polygon_pentagon():
    pentagon = RegularPolygon(5, 4)

    expected_area = (
        5 * 4**2 / (4 * math.tan(math.pi / 5))
    )

    assert pentagon.perimeter == pytest.approx(20)
    assert pentagon.area == pytest.approx(expected_area)
    assert pentagon.interior_angle == pytest.approx(3 * math.pi / 5)
    assert pentagon.exterior_angle == pytest.approx(2 * math.pi / 5)


def test_regular_polygon_hexagon():
    hexagon = RegularPolygon(6, 2)

    assert hexagon.perimeter == pytest.approx(12)
    assert hexagon.area == pytest.approx(6 * math.sqrt(3))
    assert hexagon.circumradius == pytest.approx(2)
    assert hexagon.inradius == pytest.approx(math.sqrt(3))
    assert hexagon.apothem == pytest.approx(math.sqrt(3))


def test_regular_polygon_interior_angle_sum():
    polygon = RegularPolygon(7, 3)

    assert sum(polygon.interior_angles) == pytest.approx(5 * math.pi)


def test_regular_polygon_custom_center():
    polygon = RegularPolygon(4, 2, center=(5, -3))

    assert polygon.center == (5.0, -3.0)

    center_x, center_y = polygon.center
    assert all(
        math.hypot(x - center_x, y - center_y)
        == pytest.approx(polygon.circumradius)
        for x, y in polygon.vertices
    )


def test_regular_polygon_rotation():
    first = RegularPolygon(4, 2)
    rotated = RegularPolygon(4, 2, rotation=math.pi / 4)

    assert rotated.area == pytest.approx(first.area)
    assert rotated.perimeter == pytest.approx(first.perimeter)
    assert rotated.vertices != first.vertices


def test_regular_polygon_has_equal_sides():
    polygon = RegularPolygon(8, 3)

    assert polygon.sides == pytest.approx((3,) * 8)


def test_regular_polygon_repr():
    polygon = RegularPolygon(5, 2)

    assert repr(polygon).startswith("RegularPolygon(")


@pytest.mark.parametrize("n", [0, 1, 2, -3])
def test_regular_polygon_rejects_invalid_side_count(n):
    with pytest.raises(ValueError):
        RegularPolygon(n, 2)


@pytest.mark.parametrize("n", [3.5, True, "5"])
def test_regular_polygon_rejects_noninteger_side_count(n):
    with pytest.raises(TypeError):
        RegularPolygon(n, 2)


@pytest.mark.parametrize("side_length", [0, -1, -5])
def test_regular_polygon_rejects_nonpositive_side_length(side_length):
    with pytest.raises(ValueError):
        RegularPolygon(5, side_length)


@pytest.mark.parametrize("side_length", [math.inf, math.nan])
def test_regular_polygon_rejects_nonfinite_side_length(side_length):
    with pytest.raises(ValueError):
        RegularPolygon(5, side_length)


def test_regular_polygon_rejects_boolean_side_length():
    with pytest.raises(TypeError):
        RegularPolygon(5, True)


def test_regular_polygon_rejects_invalid_center():
    with pytest.raises(ValueError):
        RegularPolygon(5, 2, center=(0, 1, 2))


def test_regular_polygon_rejects_nonfinite_rotation():
    with pytest.raises(ValueError):
        RegularPolygon(5, 2, rotation=math.inf)
