from gmtry import Triangle

triangle_a = Triangle(5, 2 ,6)
triangle_b = Triangle(5, 2 ,6)
triangle_c = Triangle(5, 3 ,6)

print(
    triangle_a.is_congruent_to(triangle_b)
) # True

print(
    triangle_b.angle_classification
) # obtuse

print(
    round(
        triangle_c.height_a, 2
    )
) # 2.99 units

print(
    triangle_a.sides
) # (5.0, 2.0, 6.0)

print(
    round(
        triangle_b.area, 2
    )
) # 4.68