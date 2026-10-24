from collections import deque

INF = float("inf")


def main():
    n = 4
    s, t = n * 2, n * 2 + 1
    mf = Dinic(n * 2 + 2)
    for i in range(n):
        mf.add_edge(s, i, 1)
        mf.add_edge(n + i, t, 1)

    mf.add_edge(0, n, 1)
    mf.add_edge(0, n + 1, 1)
    print(mf.max_flow(s, t))


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.level = [-1] * n
        self.iter_ = [iter([])] * n

    def add_edge(self, fr, to, cap):
        ea = [to, cap, None]
        ea[2] = eb = [fr, 0, ea]
        self.g[fr].append(ea)
        self.g[to].append(eb)

    def bfs(self, s):
        self.level = [-1] * self.n
        self.level[s] = 0
        dq = deque([s])
        while dq:
            v = dq.popleft()
            for to, cap, _ in self.g[v]:
                if cap and self.level[to] < 0:
                    self.level[to] = self.level[v] + 1
                    dq.append(to)

    def dfs(self, v, t, f):
        if v == t:
            return f
        for e in self.iter_[v]:
            to, cap, rev = e
            if cap > 0 and self.level[v] < self.level[to]:
                d = self.dfs(to, t, min(f, cap))
                if d:
                    e[1] -= d
                    rev[1] += d
                    return d
        return 0

    def max_flow(self, s, t):
        flow = 0
        while True:
            self.bfs(s)
            if self.level[t] < 0:
                return flow
            self.iter_ = list(map(iter, self.g))
            f = self.dfs(s, t, INF)
            while f:
                flow += f
                f = self.dfs(s, t, INF)


if __name__ == "__main__":
    main()
