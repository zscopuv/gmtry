
from gmtry import (
    Square,
    Rectangle,
    Rhombus,
    Parallelogram,
    Trapezoid,
)

square = Square(5)
print(square.area)           # 25.0
print(square.perimeter)      # 20.0
print(square.diagonals)      # (7.07.., 7.07...)
print(square.is_equilateral) # True

rectangle_a = Rectangle(8, 4)
print(rectangle_a.area)              # 32.0
print(rectangle_a.classification)    # rectangle

rectangle_b = Rectangle(8, 8)
print(rectangle_b.classification)    # square


parallelogram = Parallelogram(8, 5, 60)
print(parallelogram.area)    # 34.64
print(parallelogram.angles)  # (60, 120, 60, 120)

rhombus = Rhombus(5, 60)
print(rhombus.area)         # 21.65

trapezoid = Trapezoid(10, 6, 4, offset=1)
print(trapezoid.area)        # 32
print(trapezoid.perimeter)   # 25.12
