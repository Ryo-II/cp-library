class LinkedList:
    def __init__(self, v=None):
        self.size = 0
        pre = self.pre = []
        nex = self.nex = []
        self.val = []
        self._new_node()  # head = 0
        self._new_node()  # end = 1

        nex[0], pre[1] = 1, 0
        if v is not None:
            self.size = len(v)
            p = 0
            for i in range(len(v)):
                u = self._new_node(v[i])
                nex[p], pre[u] = u, p
                p = u
            nex[p], pre[1] = 1, p

    def _new_node(self, v=None):
        self.pre.append(None)
        self.nex.append(None)
        self.val.append(v)
        return len(self.val) - 1

    def add(self, u, v):
        """u(idx)の後にv(idx)を追加"""
        assert 0 <= u < len(self.val)
        assert 0 <= v < len(self.val)
        pre = self.pre
        nex = self.nex
        self.size += 1
        t = nex[u]
        nex[u], pre[v], nex[v], pre[t] = v, u, t, v

    def append(self, v):
        """
        末尾に値vを追加
        return: 追加されたノードのidx
        """
        vi = self._new_node(v)
        self.add(self.pre[1], vi)
        return vi

    def insert(self, u, v):
        """
        u(idx)の後に値vを追加
        return: 追加されたノードのidx
        """
        vi = self._new_node(v)
        self.add(u, vi)
        return vi

    def pop(self, v):
        """
        v(idx)を削除
        return: vの値
        """
        if self.size == 0: raise IndexError("pop from empty list")
        pre = self.pre
        nex = self.nex
        self.size -= 1
        nex[pre[v]], pre[nex[v]] = nex[v], pre[v]
        return self.val[v]

    def clear(self):
        self.size = 0
        self.nex[0], self.pre[1] = 1, 0

    def __iter__(self):
        """yield: 有効なノードのidxを先頭から"""
        nex = self.nex
        u = nex[0]
        while u != 1:
            yield u
            u = nex[u]
    def __len__(self): return self.size
    def __contains__(self, x):
        val = self.val
        for u in self:
            if val[u] == x: return True
        return False
    def __repr__(self): return f"LinkedList({' '.join(map(str, (self.val[u] for u in self)))})"
