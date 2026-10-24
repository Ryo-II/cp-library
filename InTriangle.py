"""
点 pt が 三角形 abc の内側にあるか
"""


def in_triangle(pt, a, b, c):
    b1 = sign(pt, a, b) < 0
    b2 = sign(pt, b, c) < 0
    b3 = sign(pt, c, a) < 0
    if b1 == b2 == b3:
        return True
    return False


def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
