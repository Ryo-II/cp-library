class LowLinkGraph:
    def __init__(self, n: int) -> None:
        """
        articulation : 関節点フラグのリスト (取り除くと非連結になる頂点)
        bridge : 橋フラグのリスト (取り除くと非連結になる辺)

        各連結成分ごとの答え
        """
        self._n = n
        self._e: list[tuple[int, int]] = []
        self._g: list[list[tuple[int, int]]] = [[] for _ in range(n)]
        self._ord: list[int] = []  # DFS順
        self._low: list[int] = []  # 子からたどれるmin(ord)

        self.cc_cnt = 0  # 連結成分数
        self.articulation: list[bool] = []
        self.bridge: list[bool] = []

    def add_edge(self, u: int, v: int) -> None:
        """ 無向辺の追加 """
        assert 0 <= u < self._n
        assert 0 <= v < self._n
        ei = len(self._e)
        self._e.append((u, v))
        self._g[u].append((v, ei))
        self._g[v].append((u, ei))

    def build(self) -> None:
        self._ord = [-1] * self._n
        self._low = [0] * self._n
        self.articulation = [False] * self._n
        self.bridge = [False] * len(self._e)
        k = 0
        cc = 0
        for i in range(self._n):
            if self._ord[i] == -1:
                k = self._dfs(i, k)
                cc += 1
        self.cc_cnt = cc

    def get_edge(self, i: int) -> tuple[int, int]:
        assert 0 <= i < len(self._e)
        return self._e[i]
    def get_articulations(self): return [i for i in range(self._n) if self.articulation[i]]
    def get_bridges(self): return [i for i in range(len(self._e)) if self.bridge[i]]

    def _dfs(self, u, k, ei=-1):
        self._ord[u] = k
        k += 1
        self._low[u] = self._ord[u]
        is_articulation = False
        cnt = 0
        for v, ej in self._g[u]:
            if self._ord[v] == -1:
                cnt += 1
                k = self._dfs(v, k, ej)
                if self._low[u] > self._low[v]:
                    self._low[u] = self._low[v]
                if ei != -1 and self._ord[u] <= self._low[v]:
                    is_articulation = True
                if self._ord[u] < self._low[v]:
                    self.bridge[ej] = True
            elif ej != ei:
                if self._low[u] > self._ord[v]:
                    self._low[u] = self._ord[v]
        is_articulation |= ei == -1 and cnt > 1
        self.articulation[u] = is_articulation
        return k

    def tecc(self) -> list[int]: # Two-Edge-Connected-Components
        """
        辺を1つ削除しても連結な成分
        事前にbuildしておく
        """
        self.comp = [-1] * self._n
        k = 0
        for i in range(self._n):
            if self.comp[i] != -1: continue
            self.comp[i] = k
            stack = [i]
            while stack:
                u = stack.pop()
                for v, ei in self._g[u]:
                    if self.bridge[ei]: continue
                    if self.comp[v] != -1: continue
                    self.comp[v] = k
                    stack.append(v)
            k += 1
        self.tecc_cnt = k
        return self.comp

    def tecc_groups(self) -> list[list[int]]:
        n = self.tecc_cnt + 1
        groups = [[] for _ in range(n)]
        for u in range(len(self.comp)):
            groups[self.comp[u]].append(u)
        return groups

    def tecc_tree(self) -> list[list[int]]:
        """ teccを元グラフの橋でつないだ木 """
        g = [[] for _ in range(self.tecc_cnt)]
        for ei in range(len(self._e)):
            if not self.bridge[ei]: continue
            u, v = self._e[ei]
            u = self.comp[u]
            v = self.comp[v]
            g[u].append(v)
            g[v].append(u)
        return g
