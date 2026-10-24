# mod m での a の逆元 a^{-1}
# a*a^{-1} === 1 (mod m)
# modinv(a, m) == pow(a, -1, m)
def modinv(a, m):
    b = m
    u = 1
    v = 0
    while b:
        t = a // b
        a -= t * b
        a, b = b, a
        u -= t * v
        u, v = v, u
    u %= m
    return u


# a^n (mod m)
def modpow(a, n, m):
    res = 1
    while n > 0:
        if n & 1:
            res *= a
            res %= m
        a *= a
        a %= m
        n >>= 1
    return res
