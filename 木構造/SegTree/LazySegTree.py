# # [l, r)
# # r <= n
# class LazySegTree:
#     def __init__(self, n, op=max, e=0):
#         self.size = 1 << (n - 1).bit_length()
#         self.op = op
#         self.e = e
#         self.dat = [self.e] * (self.size << 1)
#         self.lazy = [self.e] * (self.size << 1)

#     def _push(self, k, op=None):
#         if op is None:
#             op = self.op
#         if k < self.size:
#             self.lazy[k * 2] = op(self.lazy[k * 2], self.lazy[k])
#             self.lazy[k * 2 + 1] = op(self.lazy[k * 2 + 1], self.lazy[k])
#         self.dat[k] = op(self.dat[k], self.lazy[k])
#         self.lazy[k] = self.e

#     def update(self, l, r, x, op=lambda a, b: b):
#         self._update(l, r, x, 1, 0, self.size, op)

#     def get(self, l, r):
#         return self._get(l, r, 1, 0, self.size)

#     def _update(self, a, b, x, k, l, r, op):
#         self._push(k)
#         if r <= a or b <= l:
#             return
#         if a <= l and r <= b:
#             self.lazy[k] = op(self.lazy[k], x)
#             self._push(k, op)
#             return
#         self._update(a, b, x, k * 2, l, (l + r) >> 1, op)
#         self._update(a, b, x, k * 2 + 1, (l + r) >> 1, r, op)
#         self.dat[k] = self.op(self.dat[k * 2], self.dat[k * 2 + 1])

#     def _get(self, a, b, k, l, r):
#         self._push(k)
#         if r <= a or b <= l:
#             return self.e
#         if a <= l and r <= b:
#             return self.dat[k]
#         lc = self._get(a, b, k * 2, l, (l + r) >> 1)
#         rc = self._get(a, b, k * 2 + 1, (l + r) >> 1, r)
#         return self.op(lc, rc)


# if __name__ == '__main__':
#     lst = LazySegTree(128)
#     lst.update(64, 128, 20)
#     lst.update(0, 64, 10)
#     print(lst.get(63, 64))
#     print(lst.get(64, 65))


INF = 1 << 62
# https://betrue12.hateblo.jp/entry/2020/09/22/194541
# AtCoder Library を使う
from atcoder.lazysegtree import LazySegTree

# 区間加算・区間最小値
# lst = LazySegTree(min, INF, lambda f,x: x+f, lambda f,g: g+f, INF, [])

# 区間加算・区間最大値
# lst = LazySegTree(max, -INF, lambda f,x: x+f, lambda f,g: g+f, -INF, [])

# 区間変更・区間最小値
# lst = LazySegTree(min, INF, lambda f,x: x if f==INF else f, lambda f,g: g if f==INF else f, INF, [])

# 区間変更・区間最大値
# lst = LazySegTree(max, -INF, lambda f,x: x if f==-INF else f, lambda f,g: g if f==-INF else f, -INF, [])

# 区間加算・区間和

# class S:
#     def __init__(self, v=0, s=0):
#         self.v = v
#         self.s = s

# def op(x, y):
#     return S(x.v + y.v, x.s + y.s)

# def mapping(f, x):
#     x.v += f * x.s
#     return x

# def composition(f, g):
#     return g + f

# lst = LazySegTree(op, S(), mapping, composition, 0, [S(0, 1) for _ in range(n)])

# 区間変更・区間和
idt = INF

class S:
    def __init__(self, v=0, s=0):
        self.v = v
        self.s = s

def op(x, y):
    return S(x.v + y.v, x.s + y.s)

def mapping(f, x):
    if f != idt:
        x.v = f * x.s
    return x

def composition(f, g):
    if f == idt:
        return g
    else:
        return f

lst = LazySegTree(op, S(), mapping, composition, idt, [S(0, 1) for _ in range(30)])


# composition(f, g) == f(g())
