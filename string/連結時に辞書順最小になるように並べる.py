def comp(x, y):
    xl, yl = len(x[0]), len(y[0])
    if xl >= yl:
        for i in range(yl):
            if x[0][i] != y[0][i]:
                return -1 if x[0][i] < y[0][i] else 1
        if xl != yl and x[1][yl] < xl-yl:
            return -1 if x[0][yl+x[1][yl]] < x[0][x[1][yl]] else 1
        for i in range(yl):
            if y[0][i] != x[0][i+(xl-yl)]:
                return -1 if y[0][i] < x[0][i+(xl-yl)] else 1
    else:
        for i in range(xl):
            if x[0][i] != y[0][i]:
                return -1 if x[0][i] < y[0][i] else 1
        if y[1][xl] < yl-xl:
            return -1 if y[0][y[1][xl]] < y[0][xl+y[1][xl]] else 1
        for i in range(xl):
            if y[0][i+(yl-xl)] != x[0][i]:
                return -1 if y[0][i+(yl-xl)] < x[0][i] else 1
    return 0


def sort(s, reverse=False):
    from functools import cmp_to_key
    from atcoder.string import z_algorithm
    ss = [(si, z_algorithm(si)) for si in s]
    ss.sort(key=cmp_to_key(comp), reverse=reverse)
    return [si for si, _ in ss]


print(sort(["bc", "ba", "b"]))


# classを使うタイプ
from atcoder.string import z_algorithm
class S:
    __slots__ = ("s", "z")

    def __init__(self, s):
        self.s = s
        self.z = z_algorithm(s)

    def __lt__(self, other):
        sx, zx = self.s, self.z
        sy, zy = other.s, other.z
        xl, yl = len(sx), len(sy)
        if xl >= yl:
            for i in range(yl):
                if sx[i] != sy[i]:
                    return sx[i] < sy[i]
            if xl != yl and zx[yl] < xl-yl:
                return sx[yl+zx[yl]] < sx[zx[yl]]
            for i in range(yl):
                if sy[i] != sx[i+(xl-yl)]:
                    return sy[i] < sx[i+(xl-yl)]
        else:
            for i in range(xl):
                if sx[i] != sy[i]:
                    return sx[i] < sy[i]
            if zy[xl] < yl-xl:
                return sy[zy[xl]] < sy[xl+zy[xl]]
            for i in range(xl):
                if sy[i+(yl-xl)] != sx[i]:
                    return sy[i+(yl-xl)] < sx[i]
        return False


print([v.s for v in sorted([S("bc"), S("ba"), S("b")])])
