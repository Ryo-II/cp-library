INF = 1 << 61


class BitVector:
    def __init__(self, N: int) -> None:
        self.N = n = (N + 63) // 64
        self.A = [0] * (n + 1)
        self.rank64 = [0] * (n + 1)

    def set(self, i: int) -> None:
        self.A[i // 64] |= 1 << (i & 63)

    def build(self) -> None:
        for i in range(self.N):
            self.rank64[i + 1] = self.rank64[i] + self.A[i].bit_count()

    def rank(self, i: int) -> int:
        return self.rank64[i // 64] + (self.A[i // 64] & ((1 << (i & 63)) - 1)).bit_count()


class WaveletMatrix:
    def __init__(self, H: int, A: list[int]) -> None:
        self.H = H
        self.N = len(A)
        self.dat = [BitVector(self.N) for _ in range(H)]
        a = list(A)
        for h in range(H - 1, -1, -1):
            bv = self.dat[h]
            left, right = [], []
            for i in range(self.N):
                dir = a[i] >> h & 1
                (right if dir else left).append(a[i])
                if dir: bv.set(i)
            lw, rw = len(left), len(right)
            for i in range(lw): a[i] = left[i]
            for i in range(rw): a[lw + i] = right[i]
            bv.build()

    def get_subtree_range(self, h: int, l: int, r: int) -> tuple[int, int, int, int]:
        a1 = self.dat[h].rank(l)
        a0 = l - a1
        b1 = self.dat[h].rank(r)
        b0 = r - b1
        c0 = self.N - self.dat[h].rank(self.N)
        return a0, b0, c0 + a1, c0 + b1

    def kth_smallest(self, L: int, R: int, k: int) -> int:
        """ [L, R) での昇順k番目の値 """
        assert 0 <= L < R <= self.N and 0 <= k < R - L
        return self._kth_smallest(self.H, L, R, k)

    def kth_largest(self, L: int, R: int, k: int) -> int:
        """ [L, R) での降順k番目の値 """
        assert 0 <= L < R <= self.N and 0 <= k < R - L
        return self._kth_smallest(self.H, L, R, (R-L) - k - 1)

    def lt_x(self, L: int, R: int, x: int) -> int:
        """ [L, R) でのx未満の個数 """
        assert 0 <= L < R <= self.N
        return self._lt_x(self.H, L, R, 0, 1 << self.H, x)

    def range_freq(self, L: int, R: int, a: int, b: int) -> int:
        """ [L, R) でのa以上b未満の個数 """
        assert 0 <= L < R <= self.N and a < b
        return self._lt_x(self.H, L, R, 0, 1 << self.H, b) - self._lt_x(self.H, L, R, 0, 1 << self.H, a)

    def prev_value(self, L: int, R: int, x: int) -> int:
        """ x未満の最大値 なければ-INF """
        assert 0 <= L < R <= self.N
        return self._prev_value(self.H, L, R, 0, 1 << self.H, x - 1)

    def next_value(self, L: int, R: int, x: int) -> int:
        """ x以上の最小値 なければINF """
        assert 0 <= L < R <= self.N
        return self._next_value(self.H, L, R, 0, 1 << self.H, x)

    def _kth_smallest(self, h: int, l: int, r: int, k: int) -> int:
        if h == 0: return 0
        l0, r0, l1, r1 = self.get_subtree_range(h - 1, l, r)
        lw = r0 - l0
        if k < lw:
            return self._kth_smallest(h - 1, l0, r0, k)
        else:
            return (1 << (h - 1)) + self._kth_smallest(h - 1, l1, r1, k - lw)

    def _lt_x(self, h: int, l: int, r: int, a: int, b: int, x: int) -> int:
        if x <= 0: return 0
        if h == 0: return r - l
        l0, r0, l1, r1 = self.get_subtree_range(h - 1, l, r)
        c = (a + b) // 2
        if x <= c:
            return self._lt_x(h - 1, l0, r0, a, c, x)
        else:
            return r0 - l0 + self._lt_x(h - 1, l1, r1, c, b, x)

    def _prev_value(self, h: int, l: int, r: int, a: int, b: int, x: int) -> int:
        if x < 0: return -INF
        if l == r: return -INF
        if h == 0: return a
        l0, r0, l1, r1 = self.get_subtree_range(h - 1, l, r)
        c = (a + b) // 2
        if l1 != r1 and c <= x:
            rc = self._prev_value(h - 1, l1, r1, c, b, x)
            if rc != -INF: return rc
        return self._prev_value(h - 1, l0, r0, a, c, x)

    def _next_value(self, h: int, l: int, r: int, a: int, b: int, x: int) -> int:
        if l == r: return INF
        if h == 0: return a
        l0, r0, l1, r1 = self.get_subtree_range(h - 1, l, r)
        c = (a + b) // 2
        if l0 != r0 and x < c:
            lc = self._next_value(h - 1, l0, r0, a, c, x)
            if lc != INF: return lc
        return self._next_value(h - 1, l1, r1, c, b, x)


# ---------- テスト ----------

import time
import random


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} の実行時間: {(end - start)*1000:.03f}ms")
        return result
    return wrapper


@timer
def _test_kth_smallest(t, h, n):
    for _ in range(t):
        a = [random.randint(0, (1 << h) - 1) for _ in range(n)]
        wm = WaveletMatrix(h, a)
        for l in range(n):
            for r in range(l + 1, n + 1):
                b = [wm.kth_smallest(l, r, i) for i in range(r - l)]
                c = sorted(a[l:r])
                if b != c:
                    print("kth smallest")
                    print(f"{h=}, {n=}\n{a=}")
                    print(l, r)
                    print(b)
                    print(c)
                    return False
    print("complete kth smallest")
    return True

@timer
def _test_lt_x(t, h, n):
    for _ in range(t):
        a = [random.randint(0, (1 << h) - 1) for _ in range(n)]
        wm = WaveletMatrix(h, a)
        for l in range(n):
            for r in range(l + 1, n + 1):
                for x in range(1 << h):
                    b = wm.lt_x(l, r, x)
                    c = len([ai for ai in a[l:r] if ai < x])
                    if b != c:
                        print("lt x")
                        print(f"{h=}, {n=}\n{a=}")
                        print(l, r, x)
                        print(b)
                        print(c)
                        return False
    print("complete lt x")
    return True

@timer
def _test_prev_value(t, h, n):
    for _ in range(t):
        a = [random.randint(0, (1 << h) - 1) for _ in range(n)]
        wm = WaveletMatrix(h, a)
        for l in range(n):
            for r in range(l + 1, n + 1):
                aa = sorted(a[l:r])
                j = -1
                for x in range(1 << h):
                    while j+1 < len(aa) and aa[j + 1] < x:
                        j += 1
                    b = wm.prev_value(l, r, x)
                    c = aa[j] if j >= 0 else -INF
                    if b != c:
                        print("prev value")
                        print(f"{h=}, {n=}\n{a=}")
                        print(l, r, x)
                        print(b)
                        print(c)
                        return False
    print("complete prev value")
    return True

@timer
def _test_next_value(t, h, n):
    for _ in range(t):
        a = [random.randint(0, (1 << h) - 1) for _ in range(n)]
        wm = WaveletMatrix(h, a)
        for l in range(n):
            for r in range(l + 1, n + 1):
                aa = sorted(a[l:r])
                j = 0
                for x in range(1 << h):
                    while j < len(aa) and aa[j] < x:
                        j += 1
                    b = wm.next_value(l, r, x)
                    c = aa[j] if j < len(aa) else INF
                    if b != c:
                        print("next value")
                        print(f"{h=}, {n=}\n{a=}")
                        print(l, r, x)
                        print(b)
                        print(c)
                        return False
    print("complete next value")
    return True

def test():
    t = 50
    h = 5
    n = 30

    if not _test_kth_smallest(t, h, n): return
    if not _test_lt_x(t, h, n): return
    if not _test_prev_value(t, h, n): return
    if not _test_next_value(t, h, n): return

    print("*** Complete ***")

test()
