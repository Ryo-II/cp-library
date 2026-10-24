from sys import setrecursionlimit
setrecursionlimit(10**7)


class Graph:
    def __init__(self, n):
        self.g = [[] for _ in range(n)]
    def add_edge(self, s, t, c):
        self.g[s].append((t, c))

class Rerooting(Graph):
    def __init__(self, n, merge, e, leaf, apply):
        super().__init__(n)
        self.dp = []
        self.memo = []

        self.merge = merge  # merge(a, b): aとbを見て、よりよい結果を返す
        self.e = e
        self.leaf = leaf
        self.apply = apply  # apply(a, v, u, w): uから見たvのスコア (a: 頂点vでの記録, w: 辺重み)

    def run(self):
        self.memo = [self.e] * len(self.g)
        self.dp = [self.e] * len(self.g)
        self.dfs1(0, -1)
        self.dfs2(0, -1, self.e)
        return self.dp

    def dfs1(self, u, p):
        memo = self.memo
        merge = self.merge
        apply = self.apply

        upd = False
        for v, w in self.g[u]:
            if v == p: continue
            self.dfs1(v, u)
            upd = True
            memo[u] = merge(memo[u], apply(memo[v], v, u, w))
        if not upd: memo[u] = self.leaf

    def dfs2(self, u, p, val):
        g = self.g
        memo = self.memo
        merge = self.merge
        e = self.e
        apply = self.apply

        ds = [val]
        for v, w in g[u]:
            if v == p: continue
            ds.append(apply(memo[v], v, u, w))
        n = len(ds)
        idx = 1
        head = [e] * (n + 1)
        tail = [e] * (n + 1)
        for i in range(1, n + 1): head[i] = merge(head[i - 1], ds[i - 1])
        for i in range(n - 1, -1, -1): tail[i] = merge(tail[i + 1], ds[i])
        self.dp[u] = head[n]
        for v, w in g[u]:
            if v == p: continue
            sub = merge(head[idx], tail[idx + 1])
            self.dfs2(v, u, apply(sub, u, v, w))
            idx += 1


D = []

merge = max
e = 0
leaf = 0
def apply(a, v, _, w): return max(a, D[v]) + w


def main():
    n = int(input())
    g = Rerooting(n, merge, e, leaf, apply)
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        u -= 1; v -= 1
        g.add_edge(u, v, w)
        g.add_edge(v, u, w)
    global D
    D = list(map(int, input().split()))
    ans = g.run()
    print(*ans, sep="\n")


main()
