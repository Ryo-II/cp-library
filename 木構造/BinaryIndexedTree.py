class BIT:
    def __init__(self, n, op=max, e=0, a=None):
        self.size = n
        self.e = e
        self.op = op
        self.dat = [0] * (n + 1)
        if a is not None:
            for i in range(n):
                i += 1
                self.dat[i] = self.op(self.dat[i], a[i - 1])
                v = i + (i & -i)
                self.dat[v] = self.op(self.dat[v], self.dat[i])

    def apply(self, i, x): # 0 <= i < n
        i += 1
        while i <= self.size:
            self.dat[i] = self.op(self.dat[i], x)
            i += i & -i

    def prod(self, r): # [0, r)
        s = self.e
        while r > 0:
            s = self.op(s, self.dat[r])
            r -= r & -r
        return s


# 集合
class BIT_set:
    def __init__(self, n):
        self.size = n
        self.tree = [0] * (n + 1)

    def add(self, x, v=1):
        # 集合に x を加える (0 <= x < n)
        x += 1
        while x <= self.size:
            self.tree[x] += v
            x += x & -x

    def remove(self, x):
        # 集合から x を削除する
        self.add(x, -1)

    def sum(self, x):
        # x 未満の要素の数
        s = 0
        while x > 0:
            s += self.tree[x]
            x -= x & -x
        return s

    def min_k(self, k):
        # 小さいほうから k 番目(1 <= k <= n)の要素を返す
        if self.sum(self.size) < k:
            raise IndexError("BIT_set index out of range")
        i = 1 << (self.size - 1).bit_length()
        d = (i & -i)
        ret = -1
        while d:
            d >>= 1
            if i > self.size:
                i -= d
                continue
            if k > self.tree[i]:
                k -= self.tree[i]
                i += d
            else:
                if k == self.tree[i]:
                    ret = i - 1
                i -= d
        return ret

    def __getitem__(self, k):
        return self.min_k(k)

    def __contains__(self, item):
        return self.sum(item + 1) - self.sum(item) == 1


def test():
    bit = BIT(4, lambda a, b: a + b)
    bit.apply(0, 1)
    bit.apply(1, 2)
    bit.apply(2, 4)
    bit.apply(3, 8)
    print(bit.prod(0))
    print(bit.prod(1))
    print(bit.prod(2))
    print(bit.prod(3))
    print(bit.prod(4))


if __name__ == '__main__':
    test()
