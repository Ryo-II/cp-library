class Fraction:
    def __init__(self, n, d):
        if d == 0: raise ZeroDivisionError
        if d < 0:
            n, d = -n, -d
        self.n = n # 分子
        self.d = d # 分母
        self.simplification()

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def simplification(self): # 約分
        gcd = self.gcd(self.n, self.d)
        self.n //= gcd
        self.d //= gcd

    def reciprocal(self): # 逆数
        return Fraction(self.d, self.n)

    def __add__(self, other):
        if isinstance(other, int): return Fraction(self.n + other * self.d, self.d)
        if isinstance(other, Fraction): return Fraction(self.n * other.d + other.n * self.d, self.d * other.d)
        raise TypeError
    def __radd__(self, other): return self + other
    def __iadd__(self, other): return self + other

    def __sub__(self, other):
        if isinstance(other, int): return Fraction(self.n - other * self.d, self.d)
        if isinstance(other, Fraction): return Fraction(self.n * other.d - other.n * self.d, self.d * other.d)
        raise TypeError
    def __rsub__(self, other): return -self + other
    def __isub__(self, other): return self - other

    def __mul__(self, other):
        if isinstance(other, int): return Fraction(self.n * other, self.d)
        if isinstance(other, Fraction): return Fraction(self.n * other.n, self.d * other.d)
        raise TypeError
    def __rmul__(self, other): return self * other
    def __imul__(self, other): return self * other

    def __truediv__(self, other):
        if isinstance(other, int): return self * Fraction(other).reciprocal()
        if isinstance(other, Fraction): return self * other.reciprocal()
        raise TypeError
    def __rtruediv__(self, other): return other * self.reciprocal()
    def __itruediv__(self, other): return self / other

    def __neg__(self): return Fraction(-self.n, self.d)

    def _compare(self, a: "Fraction", b: "Fraction"):
        l = a.n * b.d
        r = b.n * a.d
        if l < r: return -1 # a < b
        if l > r: return 1 # a > b
        return 0 # a == b

    def __eq__(self, value): # self == value
        if isinstance(value, int): value = Fraction(value, 1)
        if isinstance(value, Fraction): return self._compare(self, value) == 0
        raise TypeError

    def __ne__(self, value): # self != value
        if isinstance(value, int): value = Fraction(value, 1)
        if isinstance(value, Fraction): return self._compare(self, value) != 0
        raise TypeError

    def __gt__(self, value): # self > value
        if isinstance(value, int): value = Fraction(value, 1)
        if isinstance(value, Fraction): return self._compare(self, value) == 1
        raise TypeError

    def __ge__(self, value): # self >= value
        if isinstance(value, int): value = Fraction(value, 1)
        if isinstance(value, Fraction): return self._compare(self, value) >= 0
        raise TypeError

    def __lt__(self, value): # self < value
        if isinstance(value, int): value = Fraction(value, 1)
        if isinstance(value, Fraction): return self._compare(self, value) == -1
        raise TypeError

    def __le__(self, value): # self <= value
        if isinstance(value, int): value = Fraction(value, 1)
        if isinstance(value, Fraction): return self._compare(self, value) <= 0
        raise TypeError

    def __int__(self): return self.n // self.d
    def __float__(self): return self.n / self.d
    def __abs__(self): return Fraction(abs(self.n), self.d)
    def __hash__(self): return hash((self.n, self.d))
    def __str__(self): return f"{self.n} / {self.d}"
    def __repr__(self): return f"Fraction({self.n}, {self.d})"


f1 = Fraction(10, 9)
print(1 - f1)
print(f1 < 1)
print(f1)
