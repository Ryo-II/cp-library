"""
備忘録
ax + by + c == 0 のイメージ :
    y = -(a/b)x + -(c/b)
    (a, b) はこの直線に垂直なベクトル

(n/m)**0.5 == n**0.5/m**0.5 等しい
"""


def p2tl(p1, p2):  # point to line
    """ 点 p1, p2 を通るような直線 ax + by + c == 0 """
    x1, y1 = p1
    x2, y2 = p2
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return (a, b, c)

def normalize_l(l): 
    """ 直線l の正規化 """
    from math import gcd
    a, b, c = l
    g = gcd(abs(a), abs(b), abs(c))
    if g != 0:
        a //= g
        b //= g
        c //= g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return (a, b, c)

def gts(a, b, c):  # general to slope
    """
    ax + by + c = 0 -> y = mx + k
    return :
        b != 0 : m, k
        b == 0 : x      # xを通るような垂直線
    """
    if b == 0: return (-c, a)
    return ((-a, b), (-c, b))

def stg(m, k):  # slope to general
    """
    y = mx + k -> ax + by + c = 0
    m, k : int | (n, d)  # 型は揃えろ
    return : (a, b, c)
    """
    if isinstance(m, tuple):
        from math import lcm
        L = lcm(m[1], k[1])
        m = m[0] * (L // m[1])
        k = k[0] * (L // k[1])
    return (m, -1, k)

def p2pbl(p1, p2):  # point to perpendicular bisector line
    """ 点 p1, p2 の垂直二等分線 ax + by + c == 0 """
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    return (
        2 * dx,
        2 * dy,
        -(dx * (x1 + x2) + dy * (y1 + y2)),
    )

def pol(p, l):  # point on line
    """ 点p が 直線l 上にあるか """
    x, y = p
    a, b, c = l
    return a*x + b*y + c == 0

def poseg(a, b, p):  # point on segment
    """ 点p が 線分ab 上にあるか """
    if cross(a, b, p) != 0: return False
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

def intersection(l1, l2):
    """ 直線 l1, l2 の交点 """
    a1, b1, c1 = l1
    a2, b2, c2 = l2
    d = a1 * b2 - a2 * b1
    if d == 0:
        return None
    x = (b1 * c2 - b2 * c1)
    y = (c1 * a2 - c2 * a1)
    if d < 0:
        d, x, y = -d, -x, -y
    return ((x, d), (y, d))

def d2_ptp(p1, p2):  # dist2 point to point
    """ p1, p2 の距離**2 """
    x1, y1 = p1
    x2, y2 = p2
    return (x1-x2)**2 + (y1-y2)**2

def d2_ptl(p, l):  # dist2 point to line
    """ 点p と 直線l の 距離**2 """
    x, y = p
    a, b, c = l
    return ((a*x + b*y + c)**2, (a**2 + b**2))

def d2_pts(p, s, t):  # dist2 point to segment
    """ 点p と 線分st の 距離**2 """
    x0, y0 = p
    x1, y1 = s
    x2, y2 = t
    if x1 == x2 and y1 == y2: return ((x1-x0)**2 + (y1-y0)**2, 1)
    a = x2 - x1
    b = y2 - y1
    r2 = a**2 + b**2
    tt = a*(x0-x1) + b*(y0-y1)
    if tt <= 0: return ((x1-x0)**2 + (y1-y0)**2, 1)
    if tt >= r2: return ((x2-x0)**2 + (y2-y0)**2, 1)
    f1 = a*(y1-y0) - b*(x1-x0)
    return (f1**2, r2)

def perpendicular_l(p, l):
    """ 点p から 直線l への垂線 """
    x, y = p
    a, b, c = l
    a2 = b
    b2 = -a
    c2 = -(a2*x + b2*y)
    return (a2, b2, c2)

def parallel_l(p, l):
    """ 点p を通る 直線l の平行線 """
    x, y = p
    a, b, c = l
    c2 = -(a*x + b*y)
    return (a, b, c2)

def cross(p1, p2, p3):
    """ 
    p1->p2 と p1->p3 の外積 (符号付き面積の2倍)
    return
        > 0 : p1->p2->p3 が反時計回り
        < 0 : 時計回り
        = 0 : 直線
    """
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def dot(p1, p2, p3):
    """ 
    p1->p2 と p1->p3 の内積
    return
        > 0 : 鋭角
        = 0 : 直角
        < 0 : 鈍角
    """
    return (p2[0] - p1[0]) * (p3[0] - p1[0]) + (p2[1] - p1[1]) * (p3[1] - p1[1])

def intersect(a, b, c, d):
    """ 線分 ab, cd の交差判定 """
    c1 = cross(a, b, c)
    c2 = cross(a, b, d)
    c3 = cross(c, d, a)
    c4 = cross(c, d, b)
    if c1 == c2 == c3 == c4:
        return (max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0]))
                and max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1])))
    return c1*c2 <= 0 and c3*c4 <= 0


#  ---------- vec (floatもあり) ----------  #


class Vec:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @classmethod
    def vec(cls, s, t):
        return cls(t[0] - s[0], t[1] - s[1])

    def normalize(self):
        x, y = self.x, self.y
        d = (x**2 + y**2)
        if d != 0:
            d **= 0.5
            self.x, self.y = x / d, y / d
        return self

    def __add__(self, other): return Vec(self.x + other[0], self.y + other[1])
    def __radd__(self, other): return Vec(other[0] + self.x, other[1] + self.y)
    def __sub__(self, other): return Vec(self.x - other[0], self.y - other[1])
    def __rsub__(self, other): return Vec(other[0] - self.x, other[1] - self.y)
    def __mul__(self, other):
        if isinstance(other, (int, float)): return Vec(self.x * other, self.y * other)
        return self.x * other[0] + self.y * other[1]

    def __getitem__(self, key):
        if key == 0: return self.x
        if key == 1: return self.y
        raise IndexError

    def __repr__(self): return f"Vec({self.x}, {self.y})"


#  ----------  デバッグ用  ----------  #


def test_basic():
    # 点と点
    assert d2_ptp((0,0), (3,4)) == 25

    # 直線生成
    l = p2tl((0,0), (1,1))  # y = x
    assert pol((2,2), l)
    assert not pol((2,3), l)

    # 距離（点→直線）
    l = (1, 0, -3)  # x = 3
    n, m = d2_ptl((0,0), l)
    assert (n/m)**0.5 == 3

    # 垂線
    pl = perpendicular_l((0,0), (1,0,-3))  # x=3 に垂直 → y=0
    assert pol((0,0), pl)

    # 平行線
    pl = parallel_l((0,0), (1,0,-3))
    assert pl[0] == 1 and pl[1] == 0


def test_geometry():
    import random

    for _ in range(1000):
        x1, y1 = random.randint(-10,10), random.randint(-10,10)
        x2, y2 = random.randint(-10,10), random.randint(-10,10)
        if (x1, y1) == (x2, y2): continue

        l = p2tl((x1,y1),(x2,y2))

        # 元の2点は必ず直線上
        assert pol((x1,y1), l)
        assert pol((x2,y2), l)

        # 垂線は直交する
        px, py = random.randint(-10,10), random.randint(-10,10)
        l2 = perpendicular_l((px,py), l)

        a1,b1,_ = l
        a2,b2,_ = l2

        # 法線ベクトルの内積 = 0
        assert a1*a2 + b1*b2 == 0


def test_distance():
    import random
    import math

    for _ in range(1000):
        p = (random.randint(-10,10), random.randint(-10,10))
        a = random.randint(-10,10)
        b = random.randint(-10,10)
        if a == 0 and b == 0: continue
        c = random.randint(-10,10)

        l = (a,b,c)

        n, m = d2_ptl(p, l)
        d1 = (n/m)**0.5

        # 公式そのまま
        d2 = abs(a*p[0] + b*p[1] + c) / math.sqrt(a*a + b*b)

        assert abs(d1 - d2) < 1e-9


if __name__ == "__main__":
    test_basic()
    test_geometry()
    test_distance()
    print("*** Complete ***")
