"""
mod 998244353 のみ

やってること
def f(a, b):
    n, m = len(a), len(b)
    res = [0] * (n + m)
    for i in range(n):
        for j in range(m):
            res[i + j] += a[i] * b[j]
    return res
"""

MOD = 998244353
G = 3  # primitive root

def ntt(a: list[int], invert: bool) -> None:
    n = len(a)

    # bit reversal
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)

        for i in range(0, n, length):
            w = 1
            for j in range(i, i + length // 2):
                u = a[j]
                v = a[j + length // 2] * w % MOD
                a[j] = (u + v) % MOD
                a[j + length // 2] = (u - v) % MOD
                w = w * wlen % MOD

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a: list[int], b: list[int]) -> list[int]:
    n = 1
    while n < len(a) + len(b):
        n <<= 1

    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))

    ntt(fa, False)
    ntt(fb, False)

    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)
    return fa[:len(a)+len(b)-1]

def convolution_square(a: list[int]) -> list[int]:
    m = len(a)

    n = 1
    while n < 2 * m - 1:
        n <<= 1

    a = a + [0] * (n - m)

    ntt(a, False)

    for i in range(n):
        a[i] = a[i] * a[i] % MOD

    ntt(a, True)
    return a[:2 * m - 1]
