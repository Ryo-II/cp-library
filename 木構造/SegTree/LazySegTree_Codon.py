def bit_length(x):
    ret = 0
    while x:
        x >>= 1
        ret += 1
    return ret

class LazySegTree:
    def __init__(self, op, e, mapping, composition, id_, v):
        self._op = op
        self._e = e
        self._mapping = mapping
        self._composition = composition
        self._id = id_

        self._n = len(v)
        self._log = bit_length(self._n - 1)
        self._size = 1 << self._log
        self._d = [self._e] * (self._size << 1)
        self._lz = [self._id] * self._size

        for i in range(self._n):
            self._d[self._size + i] = v[i]
        for i in range(self._size - 1, 0, -1):
            self._d[i] = self._op(self._d[i << 1], self._d[i << 1 | 1])

    def set(self, p, x):
        assert 0 <= p < self._n

        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        self._d[p] = x
        for i in range(1, self._log + 1):
            self._update(p >> i)

    def get(self, p):
        assert 0 <= p < self._n

        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        return self._d[p]

    def prod(self, left, right):
        assert 0 <= left <= right <= self._n

        if left == right: return self._e

        left += self._size
        right += self._size

        for i in range(self._log, 0, -1):
            if ((left >> i) << i) != left:
                self._push(left >> i)
            if ((right >> i) << i) != right:
                self._push((right - 1) >> i)

        sml = self._e
        smr = self._e
        while left < right:
            if left & 1:
                sml = self._op(sml, self._d[left])
                left += 1
            if right & 1:
                right -= 1
                smr = self._op(self._d[right], smr)
            left >>= 1
            right >>= 1

        return self._op(sml, smr)

    def all_prod(self):
        return self._d[1]

    def apply(self, left, right, f):
        assert 0 <= left <= right <= self._n
        if left == right: return
        left += self._size
        right += self._size

        for i in range(self._log, 0, -1):
            if ((left >> i) << i) != left:
                self._push(left >> i)
            if ((right >> i) << i) != right:
                self._push((right - 1) >> i)

        l2, r2 = left, right
        while left < right:
            if left & 1:
                self._all_apply(left, f)
                left += 1
            if right & 1:
                right -= 1
                self._all_apply(right, f)
            left >>= 1
            right >>= 1
        left, right = l2, r2

        for i in range(1, self._log + 1):
            if ((left >> i) << i) != left:
                self._update(left >> i)
            if ((right >> i) << i) != right:
                self._update((right - 1) >> i)

    def max_right(self, left, g):
        assert 0 <= left <= self._n
        assert g(self._e)

        if left == self._n:
            return self._n

        left += self._size
        for i in range(self._log, 0, -1):
            self._push(left >> i)

        sm = self._e
        first = True
        while first or (left & -left) != left:
            first = False
            while left % 2 == 0:
                left >>= 1
            if not g(self._op(sm, self._d[left])):
                while left < self._size:
                    self._push(left)
                    left *= 2
                    if g(self._op(sm, self._d[left])):
                        sm = self._op(sm, self._d[left])
                        left += 1
                return left - self._size
            sm = self._op(sm, self._d[left])
            left += 1

        return self._n

    def min_left(self, right, g):
        assert 0 <= right <= self._n
        assert g(self._e)

        if right == 0:
            return 0

        right += self._size
        for i in range(self._log, 0, -1):
            self._push((right - 1) >> i)

        sm = self._e
        first = True
        while first or (right & -right) != right:
            first = False
            right -= 1
            while right > 1 and right % 2:
                right >>= 1
            if not g(self._op(self._d[right], sm)):
                while right < self._size:
                    self._push(right)
                    right = 2 * right + 1
                    if g(self._op(self._d[right], sm)):
                        sm = self._op(self._d[right], sm)
                        right -= 1
                return right + 1 - self._size
            sm = self._op(self._d[right], sm)

        return 0

    def _update(self, k):
        self._d[k] = self._op(self._d[k << 1], self._d[k << 1 | 1])

    def _all_apply(self, k, f):
        self._d[k] = self._mapping(f, self._d[k])
        if k < self._size:
            self._lz[k] = self._composition(f, self._lz[k])

    def _push(self, k):
        self._all_apply(k << 1, self._lz[k])
        self._all_apply(k << 1 | 1, self._lz[k])
        self._lz[k] = self._id
