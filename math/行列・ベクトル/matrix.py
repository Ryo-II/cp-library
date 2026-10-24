from math import *


# vベクトルをtheta(rad)回転させる
def rotate(v, theta):
    c = cos(theta)
    s = sin(theta)
    return v[0] * c - v[1] * s, v[0] * s + v[1] * c


# 角度(rad)を求めるなら
def test3(a, b, c):
    ab = (a[0] - b[0], a[1] - b[1])
    ac = (a[0] - c[0], a[1] - c[1])
    dot = ab[0] * ac[0] + ab[1] * ac[1]
    return acos(dot / (dist(a, b) * dist(a, c)))


# 角度(rad)その2
def test4(a, b, c):
    ab = (a[0] - b[0], a[1] - b[1])
    ac = (a[0] - c[0], a[1] - c[1])
    return atan2(
        ab[0] * ac[1] - ab[1] * ac[0],
        ab[0] * ac[0] + ab[1] * ac[1]
    )


a = (0, 0)
b = (1, 2)
c = (1, -1)
ab = (a[0] - b[0], a[1] - b[1])
ac = (a[0] - c[0], a[1] - c[1])
print(degrees(test3(a, b, c)))
print(degrees(test4(a, b, c)))

print("rotate", rotate((1, 0), radians(90)))


class Matrix:
    def __init__(self, h, w, val=0):
        self.h = h
        self.w = w
        self.d = [[val] * w for _ in range(h)]

    @classmethod
    def unit(cls, n):
        ret = cls(n, n)
        for i in range(n):
            ret[i][i] = 1
        return ret

    def __mul__(self, a: "Matrix") -> "Matrix":
        assert self.w == a.h
        r = Matrix(self.h, a.w)
        for i in range(self.h):
            ri = r[i]
            di = self.d[i]
            for k in range(self.w):
                ak = a[k]
                for j in range(a.w):
                    ri[j] += di[k] * ak[j]
        return r
    def __pow__(self, t: int) -> "Matrix":
        assert self.h == self.w
        a = Matrix(self.h, self.h)
        for i in range(self.h):
            a.d[i] = self.d[i][:]
        r = Matrix.unit(self.h)
        for i in range(t.bit_length()):
            if t >> i & 1:
                r = r * a
            a *= a
        return r
    def __str__(self): return "[" + ", ".join(map(str, self.d)) + "]"
    def __iter__(self): yield from self.d
    def __getitem__(self, key): return self.d[key]
    def _print(self):
        for i in range(self.h):
            print(" ["[i==0] + "[" + " ".join(map(str, self.d[i])) + "]]"[i<self.h-1:])


m1 = Matrix(3, 3, 1)
m1[1][2] = 0
m1._print()
(m1 * m1 * m1)._print()
(m1 ** 3)._print()

print(m1)
for r in m1:
    print(r)
