class SegTree:
    def __init__(self, op, e, v):
        self._op = op
        self._e = e

        self._n = len(v)
        self._log = (self._n - 1).bit_length()
        self._size = 1 << self._log
        self._d = [self._e] * (self._size << 1)

        for i in range(self._n):
            self._d[self._size + i] = v[i]
        for i in range(self._size - 1, 0, -1):
            self._d[i] = self._op(self._d[i * 2], self._d[i * 2 + 1])

    def set(self, i, x):
        k = self._size + i
        self._d[k] = x
        while k > 1:
            k >>= 1
            self._d[k] = self._op(self._d[k * 2], self._d[k * 2 + 1])

    def get(self, i):
        return self._d[i + self._size]

    def all_prod(self):
        return self._d[1]

    def prod(self, l, r):
        # [l, r)
        lc = self._e
        rc = self._e
        l += self._size
        r += self._size
        while l < r:
            if l & 1:
                lc = self._op(lc, self._d[l])
                l += 1
            if r & 1:
                r -= 1
                rc = self._op(self._d[r], rc)
            l >>= 1
            r >>= 1
        return self._op(lc, rc)


def test():
    n = 20
    seg = SegTree(lambda a, b: a + b, 0, [0] * n)
    while 1:
        t, *d = map(int, input().split())
        if t == 0:
            k, v = d
            print([seg.get(i) for i in range(n)])
            seg.set(k, v)
            print([seg.get(i) for i in range(n)])
        else:
            l, r = d
            print(seg.all_prod())
            print(seg.prod(l, r))


if __name__ == '__main__':
    test()
