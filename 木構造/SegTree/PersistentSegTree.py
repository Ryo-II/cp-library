from typing import Callable, Any


class PersistentSegTree:
    def __init__(self, op: Callable[[Any, Any], Any], e: Any, v: int | list[Any]) -> None:
        self._op = op
        self._e = e

        if isinstance(v, int):
            v = [e] * v

        self._n = len(v)
        self._log = (self._n - 1).bit_length()
        self._size = 1 << self._log

        self._roots = [0]
        self._X: list[Any] = [e] * (self._size << 1)
        self._L: list[int] = [0] * (self._size << 1)
        self._R: list[int] = [0] * (self._size << 1)

        for i in range(self._n):
            self._X[self._size + i] = v[i]
        for i in range(self._size - 1, -1, -1):
            lc, rc = i << 1, i << 1 | 1
            self._X[i] = self._op(self._X[lc], self._X[rc])
            self._L[i] = lc
            self._R[i] = rc

    def _new(self, old: int) -> int:
        self._L.append(self._L[old])
        self._R.append(self._R[old])
        self._X.append(self._X[old])
        return len(self._X) - 1

    def set(self, t: int, p: int, x: Any) -> int:
        assert 0 <= p < self._n

        new = self._new(self._roots[t])
        self._roots.append(new)

        i, l, r = new, 0, self._n - 1

        stack = [(i, l, r, 0)]
        while stack:
            i, l, r, col = stack.pop()

            if l == r:
                self._X[i] = x
                continue

            if col == 0:
                stack.append((i, l, r, 1))

                mid = (l + r) >> 1
                if p <= mid:
                    self._L[i] = self._new(self._L[i])
                    stack.append((self._L[i], l, mid, 0))
                else:
                    self._R[i] = self._new(self._R[i])
                    stack.append((self._R[i], mid + 1, r, 0))
            else:
                self._X[i] = self._op(self._X[self._L[i]], self._X[self._R[i]])

        return len(self._roots) - 1

    def get(self, t: int, p: int) -> Any:
        assert 0 <= p < self._n
        i, l, r = self._roots[t], 0, self._n - 1
        while 1:
            if l == r:
                return self._X[i]
            mid = (l + r) >> 1
            if p <= mid:
                i, l, r = self._L[i], l, mid
            else:
                i, l, r = self._R[i], mid + 1, r

    def prod(self, t: int, left: int, right: int) -> Any:
        assert 0 <= left < right <= self._n

        right -= 1
        res = self._e
        stack = [(self._roots[t], 0, self._n - 1)]
        while stack:
            i, l, r = stack.pop()
            if left <= l <= r <= right:
                res = self._op(res, self._X[i])
            elif not (left > r or right < l):
                mid = (l + r) >> 1
                stack.append((self._R[i], mid + 1, r))
                stack.append((self._L[i], l, mid))

        return res

    def max_right(self, t: int, left: int, f: Callable[[Any], bool]) -> int:
        assert 0 <= left <= self._n

        if left == self._n:
            return self._n

        i = self._roots[t]
        l, r = 0, self._n - 1
        sm = self._e

        path = []

        # 下りながら left に対応する位置へ
        while True:
            if l == r:
                break
            mid = (l + r) >> 1
            if left <= mid:
                path.append((i, l, r, True))  # 左に行く
                i, l, r = self._L[i], l, mid
            else:
                path.append((i, l, r, False))  # 右に行く
                i, l, r = self._R[i], mid + 1, r

        # 登りながら探索
        while True:
            if not f(self._op(sm, self._X[i])):
                # このノードでNG → 降りる
                while l != r:
                    mid = (l + r) >> 1
                    if f(self._op(sm, self._X[self._L[i]])):
                        sm = self._op(sm, self._X[self._L[i]])
                        i, l, r = self._R[i], mid + 1, r
                    else:
                        i, l, r = self._L[i], l, mid
                return l

            sm = self._op(sm, self._X[i])

            # 次の区間へ
            while path:
                pi, pl, pr, went_left = path.pop()
                mid = (pl + pr) >> 1
                if went_left:
                    # 右部分へ
                    i, l, r = self._R[pi], mid + 1, pr
                    break
            else:
                return self._n

    def min_left(self, t: int, right: int, f: Callable[[Any], bool]) -> int:
        assert 0 <= right <= self._n

        if right == 0:
            return 0

        i = self._roots[t]
        l, r = 0, self._n - 1
        sm = self._e

        path = []

        right -= 1

        # 下る
        while True:
            if l == r:
                break
            mid = (l + r) >> 1
            if right <= mid:
                path.append((i, l, r, True))  # 左へ
                i, l, r = self._L[i], l, mid
            else:
                path.append((i, l, r, False))  # 右へ
                i, l, r = self._R[i], mid + 1, r

        # 登りながら
        while True:
            if not f(self._op(self._X[i], sm)):
                while l != r:
                    mid = (l + r) >> 1
                    if f(self._op(self._X[self._R[i]], sm)):
                        sm = self._op(self._X[self._R[i]], sm)
                        i, l, r = self._L[i], l, mid
                    else:
                        i, l, r = self._R[i], mid + 1, r
                return l + 1

            sm = self._op(self._X[i], sm)

            while path:
                pi, pl, pr, went_left = path.pop()
                mid = (pl + pr) >> 1
                if not went_left:
                    i, l, r = self._L[pi], pl, mid
                    break
            else:
                return 0
