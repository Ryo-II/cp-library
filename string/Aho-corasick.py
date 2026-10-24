from collections import deque


class AhoCorasick:
    def __init__(self, patterns):
        self.next = [{}]
        self.fail = [0]
        self.output = [[]]

        # Trie を構築
        for pattern_id, pattern in enumerate(patterns):
            node = 0

            for c in pattern:
                if c not in self.next[node]:
                    self.next[node][c] = len(self.next)
                    self.next.append({})
                    self.fail.append(0)
                    self.output.append([])

                node = self.next[node][c]

            self.output[node].append(pattern_id)

        # failure link を構築
        self._build_failure()

    def _build_failure(self):
        queue = deque()

        # root の子の fail は root
        for child in self.next[0].values():
            queue.append(child)
            self.fail[child] = 0

        while queue:
            node = queue.popleft()

            for c, child in self.next[node].items():
                queue.append(child)

                # failure link を辿って c が見つかるところを探す
                f = self.fail[node]

                while f != 0 and c not in self.next[f]:
                    f = self.fail[f]

                if c in self.next[f]:
                    self.fail[child] = self.next[f][c]
                else:
                    self.fail[child] = 0

                # failure 先で終わるパターンも出力対象
                self.output[child].extend(
                    self.output[self.fail[child]]
                )

    def search(self, text):
        result = []
        node = 0

        for i, c in enumerate(text):
            # 遷移できるまで failure link を辿る
            while node != 0 and c not in self.next[node]:
                node = self.fail[node]

            if c in self.next[node]:
                node = self.next[node][c]
            else:
                node = 0

            # 現在位置でマッチしたパターン
            for pattern_id in self.output[node]:
                result.append((i, pattern_id))

        return result


patterns = [
    "he",
    "she",
    "his",
    "hers",
]

ac = AhoCorasick(patterns)

text = "ahishers"

for end, pattern_id in ac.search(text):
    pattern = patterns[pattern_id]
    start = end - len(pattern) + 1

    print(start, end, pattern)