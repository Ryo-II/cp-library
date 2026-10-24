from typing import Union, SupportsInt
from random import randint


class RH:
    MOD = (1 << 61) - 1
    BASE = randint(2, MOD - 2)
    BASE_INV = pow(BASE, -1, MOD)
    m = [1]
    mi = [1]

    def __init__(self, v: Union[SupportsInt, list[SupportsInt], tuple[SupportsInt], "RH"], size: int=None):
        self.h: int = 0
        match v:
            case int(): self.h = v
            case list() | tuple(): self.h = self._hash(v)
            case RH(): self.h = v.h
            case x: raise TypeError(f"{type(x)} は未対応")
        self.size = size if size is not None else len(v)

    def pow_base(self, i: int) -> int:
        while len(RH.m) <= i:
            RH.m.append(RH.m[-1] * RH.BASE % RH.MOD)
        return RH.m[i]

    def pow_inv(self, i: int) -> int:
        while len(RH.mi) <= i:
            RH.mi.append(RH.mi[-1] * RH.BASE_INV % RH.MOD)
        return RH.mi[i]

    def _hash(self, v: Union[list[SupportsInt], tuple[SupportsInt]]) -> int:
        ret = 0
        for vi in v:
            ret = (ret * RH.BASE + vi) % RH.MOD
        return ret

    def popleft(self, c: int) -> None:
        assert self.size > 0
        self.h = (self.h - c * self.pow_base(self.size - 1)) % RH.MOD
        self.size -= 1

    def popright(self, c: int) -> None:
        assert self.size > 0
        self.h = (self.h - c) * RH.BASE_INV % RH.MOD
        self.size -= 1

    def appendleft(self, c: int) -> None:
        self.h = (self.h + c * self.pow_base(self.size)) % RH.MOD
        self.size += 1

    def appendright(self, c: int) -> None:
        self.h = (self.h * RH.BASE + c) % RH.MOD
        self.size += 1

    def extendleft(self, rh: "RH") -> None:
        self.h = (self.h + self.pow_base(self.size) * rh.h) % RH.MOD
        self.size += rh.size

    def extendright(self, rh: "RH") -> None:
        self.h = (self.h * self.pow_base(rh.size) + rh.h) % RH.MOD
        self.size += rh.size

    def copy(self): return RH(self)

    def __add__(self, rh: "RH") -> "RH": return RH((self.h * self.pow_base(rh.size) + rh.h) % RH.MOD, self.size + rh.size)
    def __radd__(self, rh: "RH") -> "RH": return RH((rh.h * self.pow_base(self.size) + self.h) % RH.MOD, rh.size + self.size)
    def __iadd__(self, rh: "RH") -> "RH":
        self.h = (self.h * self.pow_base(rh.size) + rh.h) % RH.MOD
        self.size += rh.size
        return self
    def __sub__(self, rh: "RH") -> "RH": return RH((self.h - rh.h * self.pow_base(self.size - rh.size)) % RH.MOD, self.size - rh.size)
    def __rsub__(self, rh: "RH") -> "RH": return RH((rh.h - self.h * self.pow_base(rh.size - self.size)) % RH.MOD, rh.size - self.size)
    def __isub__(self, rh: "RH") -> "RH":
        self.h = (self.h - rh.h) * self.pow_inv(rh.size) % RH.MOD
        self.size -= rh.size
        return self
    def __eq__(self, rh: "RH") -> bool: return self.size == rh.size and self.h == rh.h
    def __ne__(self, rh: "RH") -> bool: return self.size != rh.size or self.h != rh.h
    def __bool__(self): return self.size != 0
    def __len__(self): return self.size
    def __repr__(self): return f"RH(v=[{self.h}], size={self.size})"
    def __str__(self): return f"RH(hash: {self.h}, size: {self.size})"


m1 = RH([97])
m2 = RH([98])
m3 = RH([99])
print((m1+m2)+m3 == m1+(m2+m3), True)

s1 = RH([97])
s2 = RH([98])
s3 = RH([97, 98])
print(f"s1 == s3 : {s1 == s3} : need False")
print(f"s3 == s1 + s2 : {s3 == s1 + s2} : need True")
print(f"s3 == s2 + s1 : {s3 == s2 + s1} : need False")
s1.appendright(98)
s2.appendleft(97)
print(f"s1 == s2 == s3 : {s1 == s2 == s3} : need True")
s1.popleft(97)
s2.popright(98)
print(s1 == RH([98]), True)
print(s2 == RH([97]), True)
t1 = RH([], 0)
t2 = RH(0, 0)
t4 = RH(s1, 0)
print(t1)
print(t2)
print(t4)

print(t1 + s1 == s1, True)
print(s1 + t1 == s1, True)

r1 = RH([1, 2, 3, 4, 5])
r2 = RH([1, 2])
print(f"[1,2,3,4,5] - [1,2] == [3,4,5]: {r1 - r2 == RH([3, 4, 5])} : need True")
r2.extendright(RH([3, 4, 5]))
print(r1 == r2, True)
r3 = RH([4, 5])
r3.extendleft(RH([1, 2, 3]))
print(r1 == r3, True)

print("ここまで 以下例外処理")
t_err = RH("abc")
