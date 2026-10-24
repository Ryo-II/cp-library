def comb(n, r):
    r = min(r, n - r)
    if r == 0:
        return 1
    if r == 1:
        return n

    numerator = [n - r + k + 1 for k in range(r)]
    denominator = [k + 1 for k in range(r)]

    for p in range(2, r + 1):
        pivot = denominator[p - 1]
        if pivot > 1:
            offset = (n - r) % p
            for k in range(p - 1, r, p):
                numerator[k - offset] //= pivot
                denominator[k] //= pivot

    result = 1
    for k in range(r):
        if numerator[k] > 1:
            result *= numerator[k]
    return result


def comb_under5000(mod):
    MAX = 5000
    comb = [[0] * (i + 2) for i in range(MAX + 1)]
    for i in range(MAX + 1):
        comb[i][0] = 1
        for j in range(1, i + 1):
            comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % mod
    return comb


class Combinations:
    __slots__ = ["mod", "fact", "inv"]
    def __init__(self, n, mod):
        self.mod = mod
        self.fact = [0] * (n + 1)
        self.fact[0] = 1
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv = [0] * (n + 1)
        self.inv[n] = self.modinv(self.fact[n])
        for i in range(n, 0, -1):
            self.inv[i - 1] = self.inv[i] * i % mod

    def modinv(self, a):
        b = self.mod
        u = 1
        v = 0
        while b:
            t = a // b
            a -= t * b
            a, b = b, a
            u -= t * v
            u, v = v, u
        u %= self.mod
        return u

    def perm(self, n, r):
        if r < 0 or n < r: return 0
        return self.fact[n] * self.inv[n - r] % self.mod

    def comb(self, n, r):
        if r < 0 or n < r: return 0
        return self.fact[n] * self.inv[r] % self.mod * self.inv[n - r] % self.mod

    def hom(self, n, r):
        return self.comb(n + r - 1, r)

    def comb2(self, n, r):  # rが小さい場合 Combinations(max(r), mod) とする
        if r < 0 or n < r: return 0
        ret = 1
        for i in range(n, n-r, -1):
            ret = ret * i % self.mod
        ret = ret * self.inv[r] % self.mod
        return ret


print(Combinations(10, 998244353).comb(0, 0))

"""
nPr = n! / (n - r)! = mul(range(n, n-r, -1))   nが大きくrが小さい場合はこれが使える
nCr = n! / (r! * (n - r)!)
nCr = nPr / r!
nCr = n-1Cr-1 + n-1Cr
nHr = C(n+r-1, r) = C(n+r-1, n-1)
"""

"""
一見複雑な時はほかの方法も考えること！ DPとか
・N個のグループがあり、違うグループからk個選ぶ
    dp[i][j] : i番目まで見てすでにj個選んでいる場合の数
        dp[i+1][j] += dp[i][j]
        dp[i+1][j+1] += dp[i][j] * A[i]
"""

"""
総乗

k個のボール を n個の箱 に振り分け、∏(a) の総和を求める
a = [a_0, a_1, ... , a_(n-1)]

ans = 0
for a in (sum(a) == k であるようなすべてのa):
    now = 1
    for i in range(n):
        now *= a[i]
    ans += now

ans == comb((n-1) + n + (k-n), k - n) == comb(k + n - 1, k - n)
 : k個のボール を n個の箱 に分けたのち、各箱から区別してどれか1個のボールを選ぶ方法の数
    == comb((n-1個の仕切り + n個の選んだボール) + 選んでいないボール, 選んでいないボール)
"""
