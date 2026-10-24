class mint:
    MOD = 998244353
    def __init__(self, x=0):
        self.x: int = int(x) % self.MOD

    # mod m での a の逆元 a^{-1}
    # a*a^{-1} === 1 (mod m)
    # modinv(a, m) == pow(a, -1, m)
    def _modinv(self, a: int) -> int:
        a = int(a)
        b = self.MOD
        u = 1
        v = 0
        while b:
            t = a // b
            a -= t * b
            a, b = b, a
            u -= t * v
            u, v = v, u
        u %= self.MOD
        return u

    # a^n (mod m)
    def _modpow(self, a: int, n: int) -> int:
        res = 1
        while n > 0:
            if n & 1:
                res *= a
                res %= self.MOD
            a *= a
            a %= self.MOD
            n >>= 1
        return res

    def __add__(self, other): return mint(self.x + int(other))
    def __radd__(self, other): return mint(int(other) + self.x)
    def __iadd__(self, other):
        self.x = (self.x + int(other)) % self.MOD
        return self

    def __sub__(self, other): return mint(self.x - int(other))
    def __rsub__(self, other): return mint(int(other) - self.x)
    def __isub__(self, other):
        self.x = (self.x - int(other)) % self.MOD
        return self

    def __mul__(self, other): return mint(self.x * int(other))
    def __rmul__(self, other): return mint(int(other) * self.x)
    def __imul__(self, other):
        self.x = (self.x * int(other)) % self.MOD
        return self

    def __truediv__(self, other): return mint(self.x * self._modinv(int(other)))
    def __rtruediv__(self, other): return mint(int(other) * self._modinv(self.x))
    def __itruediv__(self, other):
        self.x = (self.x * self._modinv(int(other))) % self.MOD
        return self

    def __mod__(self, other): return mint(self.x % int(other))
    def __rmod__(self, other): return mint(int(other) % self.x)
    def __imod__(self, other):
        self.x = (self.x % int(other)) % self.MOD
        return self

    def __pow__(self, n):
        n = int(n)
        if n < 0:
            return mint(self._modinv(self._modpow(self.x, -n)))
        return mint(self._modpow(self.x, n))
    def __rpow__(self, a): return mint(self._modpow(int(a), self.x))
    def __ipow__(self, n):
        n = int(n)
        if n < 0:
            self.x = self._modinv(self._modpow(self.x, -n))
        else:
            self.x = self._modpow(self.x, n)
        return self

    def __eq__(self, value): return self.x == int(value)
    def __ne__(self, value): return self.x != int(value)

    def __int__(self): return self.x
    def __str__(self): return str(self.x)
    def __repr__(self): return f"mint({self.x})"


a = 4456
n = 233
test = mint(a)
print(test.__repr__())
print(test ** n)
print(pow(a, n, 998244353))

print(mint(1) == mint(1))

x, y = mint(7), mint(11)
a, b = 13, 17
print(x + y)
print(x + b)
print(a + y)
print(a + b)

print((x ** -1) * x == 1)

