# 最大公約数を求める
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 最小公倍数を求める
def lcm(a, b):
    u, v = a, b
    while v:
        u, v = v, u % v
    return a * b // u


"""
ax + by = c の整数解
g = gcd(a, b)
整数解を持つ条件: c % g == 0
ax + by = g を満たす x, y = ext_gcd(a, b)
c//g 倍する
"""
# def ext_gcd(a, b):
#     if b == 0:
#         return a, 1, 0
#     d, y, x = ext_gcd(b, a % b)
#     y -= a // b * x
#     return d, x, y
def ext_gcd(a, b):
    x, u = 0, 1
    y, v = 1, 0
    while b:
        t = a // b
        a, b = b, a % b
        x, u = u - t * x, x
        y, v = v - t * y, y
    return u, v


a, b = 42, 60
x, y = ext_gcd(a, b)
print(f"{a}*{x} + {b}*{y} = {a*x + b*y}", f"{gcd(a,b)=}")
