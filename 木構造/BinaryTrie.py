INF = 1 << 61


class BinaryTrie:
    def __init__(self, h: int, a: "list[int] | None"=None) -> None:
        self.h = h
        self.size = 0
        self.root = self.e()
        if a is not None:
            for ai in a:
                self.add(ai)

    @staticmethod
    def e():
        return [None, None, 0]

    def add(self, i: int) -> None:
        """ Trieにiを追加 """
        h = self.h
        u = self.root
        for h in range(h - 1, -1, -1):
            u[2] += 1
            v = i >> h & 1
            if u[v] is None: u[v] = self.e()
            u = u[v]
        else:
            u[2] += 1
        self.size += 1

    def remove(self, i: int) -> None:
        """ Trieからiを削除"""
        if self.size == 0: raise IndexError("remove from empty Trie")
        u = self.root
        for h in range(self.h - 1, -1, -1):
            v = i >> h & 1
            if u[v] is None or u[v][2] == 0: raise ValueError(f"{i} not in Trie")
            u[2] -= 1
            u = u[v]
        else:
            u[2] -= 1
        self.size -= 1

    def kth_smallest(self, k: int, xor: int=0) -> int:
        """ 昇順k番目 """
        assert 0 <= k < self.size and xor < 1 << self.h
        h = self.h
        u = self.root
        res = 0
        for h in range(h - 1, -1, -1):
            x = xor >> h & 1
            lc = u[x][2]  if u[x] is not None else 0
            if k < lc:
                u = u[x]
            else:
                res += 1 << h
                u = u[x ^ 1]
                k -= lc
        return res

    def kth_largest(self, k: int, xor: int=0) -> int:
        """ 降順k番目 """
        assert 0 <= k < self.size and xor < 1 << self.h
        return self.kth_smallest(self.h, self.root, self.size - k - 1, xor)

    def lt_x(self, x: int) -> int:
        """ x未満の個数 """
        if x <= 0: return 0
        h = self.h
        u = self.root
        l, r = 0, 1 << h
        res = 0
        for h in range(h - 1, -1, -1):
            mid = (l + r) // 2
            if x <= mid:
                if u[0] is None: break
                u = u[0]
                r = mid
            else:
                res += u[0][2] if u[0] is not None else 0
                if u[1] is None: break
                u = u[1]
                l = mid
        else:
            res += u[2]
        return res

    def range_freq(self, l: int, r: int) -> int:
        """ l以上r未満の個数 """
        assert l < r
        return self.lt_x(r) - self.lt_x(l)

    def prev_value(self, x: int) -> int:
        """ x未満の最大値 なければ-INF """
        return self._prev_value(self.h, self.root, 0, 1 << self.h, x - 1)

    def next_value(self, x: int) -> int:
        """ x以上の最小値 なければINF """
        return self._next_value(self.h, self.root, 0, 1 << self.h, x)

    def _prev_value(self, h: int, u: list, l: int, r: int, x: int) -> int:
        if x < 0: return -INF
        if h == 0: return l if u[2] > 0 else -INF
        mid = (l + r) // 2
        if mid <= x and u[1] is not None:
            rc = self._prev_value(h - 1, u[1], mid, r, x)
            if rc != -INF: return rc
        if u[0] is None: return -INF
        return self._prev_value(h - 1, u[0], l, mid, x)

    def _next_value(self, h: int, u: list, l: int, r: int, x: int) -> int:
        if h == 0: return l if u[2] > 0 else INF
        mid = (l + r) // 2
        if x < mid and u[0] is not None:
            lc = self._next_value(h - 1, u[0], l, mid, x)
            if lc != INF: return lc
        if u[1] is None: return INF
        return self._next_value(h - 1, u[1], mid, r, x)

    # ---- デバッグ/出力 用 ----

    def get_list(self):
        res = []
        stack = [(self.h, self.root, 0)]
        while stack:
            h, u, x = stack.pop()
            if h == 0:
                res.extend([x] * u[2])
                continue
            if u[2] == 0:
                continue
            if u[1] is not None:
                stack.append((h - 1, u[1], (1 << (h - 1)) + x))
            if u[0] is not None:
                stack.append((h - 1, u[0], x))
        return res


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
def _test_add_remove(t, h, n):
    for _ in range(t):
        a = [random.randint(0, (1 << h) - 1) for _ in range(n)]
        bt = BinaryTrie(h)
        for i in range(n):
            bt.add(a[~i])
        s = sorted(a)
        for i in range(n + 1):
            b = bt.get_list()
            if bt.get_list() != s:
                print("get list")
                print(f"{h=}, {n=}\n{a=}\n{s=}\n{b=}")
                return False
            if i < n:
                bt.remove(a[i])
                s.remove(a[i])
    print("complete add remove")
    return True

@timer
def _test_kth_smallest(t, h, n):
    for _ in range(t):
        a = [random.randint(0, (1 << h) - 1) for _ in range(n)]
        bt = BinaryTrie(h, a)
        b = [bt.kth_smallest(i) for i in range(n)]
        s = sorted(a)
        if s != b:
            print("kth smallest")
            print(f"{h=}, {n=}\n{a=}\n{s=}\n{b=}")
            return False
    print("complete kth smallest")
    return True

@timer
def _test_lt_x(t, h, n):
    for _ in range(t):
        a = [random.randint(0, (1 << h) - 1) for _ in range(n)]
        bt = BinaryTrie(h, a)
        for x in range(n):
            b = bt.lt_x(x)
            c = len([1 for ai in a if ai < x])
            if b != c:
                print("lt x")
                s = sorted(a)
                print(f"{h=}, {n=}, {x=}\n{a=}\n{s=}\n{b=}, {c=}")
                return False
    print("complete lt x")
    return True

@timer
def _test_prev_value(t, h, n):
    for _ in range(t):
        a = [random.randint(0, (1 << h) - 1) for _ in range(n)]
        bt = BinaryTrie(h, a)
        s = sorted(a)
        j = -1
        for x in range(n):
            while j + 1 < n and s[j + 1] < x:
                j += 1
            b = bt.prev_value(x)
            c = s[j] if j >= 0 else -INF
            if b != c:
                print("prev value")
                print(f"{h=}, {n=}, {x=}\n{a=}\n{s=}\n{b=}, {c=}")
                return False
    print("complete prev value")
    return True

@timer
def _test_next_value(t, h, n):
    for _ in range(t):
        a = [random.randint(0, (1 << h) - 1) for _ in range(n)]
        bt = BinaryTrie(h, a)
        s = sorted(a)
        j = 0
        for x in range(n):
            while j < n and s[j] < x:
                j += 1
            b = bt.next_value(x)
            c = s[j] if j < n else INF
            if b != c:
                print("next value")
                print(f"{h=}, {n=}, {x=}\n{a=}\n{s=}\n{b=}, {c=}")
                return False
    print("complete next value")
    return True

def test():
    t = 1000
    h = 6
    n = 60

    if not _test_add_remove(t, h, n): return
    if not _test_kth_smallest(t, h, n): return
    if not _test_lt_x(t, h, n): return
    if not _test_prev_value(t, h, n): return
    if not _test_next_value(t, h, n): return

    print("*** Complete ***")

test()
