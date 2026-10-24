from sys import setrecursionlimit
from collections import deque

setrecursionlimit(10 ** 9 + 7)
INF = 1 << 62


class LCA:
    def __init__(self, n, g, root=0):
        self.size = n
        self.par = [[] for _ in range(self.size)]
        self.dep = [INF] * self.size

        dq = deque([(root, 0)])
        while dq:
            u, d = dq.popleft()
            if self.par[u]:
                j = 0
                p = self.par[u][j]
                while len(self.par[p]) > j:
                    p = self.par[p][j]
                    self.par[u].append(p)
                    j += 1
            self.dep[u] = d
            for v in g[u]:
                if self.dep[v] <= d + 1: continue
                self.par[v].append(u)
                dq.append((v, d + 1))

    def lca(self, u, v):
        if self.dep[u] < self.dep[v]:
            u, v = v, u
        sub = self.dep[u] - self.dep[v]
        for i in range(sub.bit_length()):
            if sub >> i & 1:
                u = self.par[u][i]
        if u == v:
            return u
        for i in range(self.dep[u].bit_length(), -1, -1):
            if len(self.par[u]) > i and self.par[u][i] != self.par[v][i]:
                u = self.par[u][i]
                v = self.par[v][i]
        return self.par[u][0]

    def dist(self, u, v):
        return self.dep[u] + self.dep[v] - self.dep[self.lca(u, v)] * 2
