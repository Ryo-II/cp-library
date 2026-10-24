class DualSegTree:
    def __init__(self, n, op, e):
        self.size = 1 << (n - 1).bit_length()
        self.op = op
        self.e = e
        self.dat = [e] * (self.size << 1)

    def apply(self, l, r, x):
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                self.dat[l] = self.op(self.dat[l], x)
                l += 1
            if r & 1:
                self.dat[r - 1] = self.op(self.dat[r - 1], x)
            l >>= 1
            r >>= 1

    def get(self, i):
        i += self.size
        ret = self.e
        while i > 0:
            ret = self.op(ret, self.dat[i])
            i >>= 1
        return ret
