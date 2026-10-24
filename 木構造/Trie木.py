"""
文字列を木構造で持つ
"""


class Trie:
    class Node:
        def __init__(self):
            self.to = dict()
            self.cnt = 0

    def __init__(self):
        self.d: list[Trie.Node] = [self.Node()]

    def add(self, s):
        v = 0
        for c in s:
            if c not in self.d[v].to:
                self.d[v].to[c] = len(self.d)
                self.d.append(self.Node())
            v = self.d[v].to[c]
        self.d[v].cnt += 1
