class UnionFind:
    def __init__(self, n):
        self.n = n
        self.gc = n
        self.par = [-1] * n  # par[i] < 0 ならサイズ par[i] >= 0 なら親

    def root(self, a):
        x = a
        while self.par[x] >= 0:
            x = self.par[x]
        while a != x:
            self.par[a], a = x, self.par[a]
        return x

    def merge(self, a, b):
        a = self.root(a)
        b = self.root(b)
        if a == b:
            return False
        if self.par[a] > self.par[b]:
            a, b = b, a
        self.gc -= 1
        self.par[a] += self.par[b]
        self.par[b] = a
        return True

    def same(self, a, b): return self.root(a) == self.root(b)
    def size(self, a): return -self.par[self.root(a)]
    def leaders(self): return [i for i in range(self.n) if self.par[i] < 0]
    def members(self, a): return [i for i in range(self.n) if self.same(a, i)]
    def group_count(self): return self.gc
    def groups(self):
        res = [[] for _ in range(self.n)]
        for i in range(self.n):
            res[self.root(i)].append(i)
        return res
    def __getitem__(self, a): return self.root(a)
