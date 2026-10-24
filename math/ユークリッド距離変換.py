"""

https://paiza.jp/challenges/728/retry

"""



from sys import stdin, stderr, setrecursionlimit
from collections import deque, defaultdict, Counter
from bisect import bisect_left, bisect_right
from heapq import heapify, heappop, heappush, heappushpop
from math import gcd, lcm, factorial
from itertools import permutations, accumulate, product, combinations
from functools import cache, reduce, cmp_to_key
from random import randint, shuffle

setrecursionlimit(10 ** 8)
input = stdin.readline
INF = 1 << 61
INf = float("inf")
MOD99 = 998244353
MOD17 = 1000000007
MOD61 = (1 << 61) - 1

DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)
DX8 = (0, 1, 1, 1, 0, -1, -1, -1)
DY8 = (-1, -1, 0, 1, 1, 1, 0, -1)

def clamp(lo, x, hi): return max(lo, min(x, hi))
# def m_rot_r(a): return list(zip(*a[::-1]))  # 時計回り
def m_rot_l(a): return list(zip(*[row[::-1] for row in a]))  # 反時計回り
def interval_mask(s, l, r, w):  # [s, s+w) ∩ [l, r) をbitで返す
    L, R = clamp(0, l - s, w), clamp(0, r - s, w)
    if L >= R: return 0
    return ((1 << R) - 1) ^ ((1 << L) - 1)

def yes(f=True): print("Yes" if f else "No")
def no(f=True): print("No" if f else "Yes")


def edt_1d(f):
    """
    1 次元 Euclidean Distance Transform
    f[i] = 0 なら点がある、INF なら点がない

    戻り値:
        d[i] = min_j ( (i - j)^2 + f[j] )
    """
    n = len(f)

    # v[k] : k 番目に採用された放物線の中心 index
    v = [0] * n

    # z[k] : v[k] と v[k+1] の境界（交点）
    z = [0.0] * (n + 1)

    # 採用された放物線の数 - 1
    k = 0
    v[0] = 0
    z[0] = -INf
    z[1] = INf

    # 放物線の下包絡線を構築
    for q in range(1, n):
        # v[k] と q の放物線の交点を計算
        while True:
            # 交点 x 座標（連続値）
            s = ((f[q] + q*q) - (f[v[k]] + v[k]*v[k])) / (2*q - 2*v[k])

            """
x = v[k]
f[q] + (i-q)**2 == f[x] + (i-x)**2
f[q] - 2iq + q**2 == f[x] - 2ix + x**2
2iq - 2ix == -f[x] - x**2 + f[q] + q**2
2i(q - x) == f[q]-f[x] + q**2-x**2
i == (f[q]-f[x] + q**2-x**2) / 2(q-x)
            """

            # 交点が左に行きすぎたら、直前の放物線は不要
            if s <= z[k]:
                k -= 1
                if k < 0:
                    k = 0
                    break
            else:
                break

        k += 1
        v[k] = q
        z[k] = s
        z[k+1] = INf

    # 各 i について最小値を計算
    d = [0] * n
    k = 0
    for i in range(n):
        # i がどの放物線区間に属するか
        while z[k+1] < i:
            k += 1
        j = v[k]
        d[i] = (i - j)**2 + f[j]

    return d


def main():
    h, w = map(int, input().split())
    s = ["." * (w + 2)]
    for _ in range(h):
        s.append("." + input()[:-1] + ".")
    s.append("." * (w + 2))
    h += 2; w += 2

    col_dist = [[0] * w for _ in range(h)]
    for j in range(w):
        f = [0 if s[i][j] == "." else INF for i in range(h)]
        d = edt_1d(f)
        for i in range(h):
            col_dist[i][j] = d[i]

    print(*col_dist, sep="\n")

    dist = [[0] * w for _ in range(h)]
    for i in range(h):
        f = col_dist[i]
        d = edt_1d(f)
        for j in range(w):
            dist[i][j] = d[j]
    print()
    print(*dist, sep="\n")

    ans = 0
    for i in range(h):
        for j in range(w):
            ans = max(ans, dist[i][j])
    print(ans ** 0.5)


if __name__ == "__main__":
    main()
