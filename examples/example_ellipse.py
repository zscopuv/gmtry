
from gmtry import Ellipse, Circle

ellipse = Ellipse(5, 3)
print(ellipse.area)                  # 47.1238...
print(ellipse.circumference)         # 25.5269...
print(ellipse.eccentricity)          # 0.8
print(ellipse.focal_distance)        # 4.0
print(ellipse.foci)                  # ((-4.0, 0.0), (4.0, 0.0))
print(ellipse.contains_point(2, 1))  # True

circle = Circle(5)
print(circle.area)                  # 78.5398...
print(circle.circumference)         # 31.4159...
print(circle.diameter)              # 10.0
print(circle.is_unit_circle)        # False
print(circle.is_circle)             # True
print(isinstance(circle, Ellipse))  # True
