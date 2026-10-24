class FunctionalGraph:
    def __init__(self, g: list[int]):
        """g: iからg[i]への辺(0<=i<N)"""
        self.g = g
        n = self.n = len(g)
        rev = self.rev = [[] for _ in range(n)]

        cycles = self.cycles = []
        cycle_pos = self.cycle_pos = [-1] * n
        cycle_id = self.cycle_id = [-1] * n
        root = self.root = [-1] * n
        order = self.order = []
        self._dist_to_cycle = None
        self._component_size = None
        self._subtree_size = None

        _d = [0] * n
        for i in range(n):
            _d[g[i]] += 1
            rev[g[i]].append(i)

        from collections import deque
        dq = deque()
        for i in range(n):
            if _d[i] == 0:
                dq.append(i)
        while dq:
            u = dq.popleft()
            order.append(u)
            v = g[u]
            _d[v] -= 1
            if _d[v] == 0:
                dq.append(v)

        for i in range(n):
            if _d[i] == 0: continue
            if cycle_id[i] != -1: continue
            cid = len(self.cycles)
            cycles.append([])
            u = i
            while cycle_id[u] == -1:
                cycle_pos[u] = len(cycles[-1])
                cycles[-1].append(u)
                root[u] = u
                cycle_id[u] = cid
                u = g[u]

        for v in reversed(order):
            u = g[v]
            root[v] = root[u]
            cycle_id[v] = cycle_id[u]

    def in_cycle(self, v) -> bool:
        return self.cycle_pos[v] != -1

    @property
    def dist_to_cycle(self) -> list[int]:
        if self._dist_to_cycle is not None: return self._dist_to_cycle
        dist_to_cycle = self._dist_to_cycle = [0] * self.n
        g = self.g
        for v in reversed(self.order):
            dist_to_cycle[v] = dist_to_cycle[g[v]] + 1
        return dist_to_cycle

    @property
    def component_size(self) -> list[int]:  # len==N ではなく len==cycles なので注意
        """連結成分のサイズ"""
        if self._component_size is not None: return self._component_size
        component_size = self._component_size = [0] * len(self.cycles)
        cycle_id = self.cycle_id
        for v in range(self.n):
            component_size[cycle_id[v]] += 1
        return component_size

    @property
    def subtree_size(self) -> list[int]:
        """v を根とする逆木の頂点数 (自身を含む)"""
        if self._subtree_size is not None: return self._subtree_size
        subtree_size = self._subtree_size = [1] * self.n
        g = self.g
        for v in self.order:
            subtree_size[g[v]] += subtree_size[v]
        return subtree_size