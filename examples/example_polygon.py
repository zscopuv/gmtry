from gmtry import Polygon, RegularPolygon

pentagon = RegularPolygon(5, 4)

print(pentagon.area)
print(pentagon.perimeter)
print(pentagon.inradius)
print(pentagon.interior_angle)

custom = Polygon([
    (0, 0),
    (4, 0),
    (3, 2),
    (0, 2),
])

print(custom.area)       # 6.0
print(custom.perimeter)
print(custom.is_convex)
print(custom.contains_point(1, 1))