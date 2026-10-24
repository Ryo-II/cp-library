def angle_cross(p, q):  # (x, y)
    hp = 0 if (p[1] > 0 or (p[1] == 0 and p[0] > 0)) else 1
    hq = 0 if (q[1] > 0 or (q[1] == 0 and q[0] > 0)) else 1
    if hp != hq: return hp - hq

    cross = p[0] * q[1] - p[1] * q[0]
    if cross < 0: return 1
    if cross > 0: return -1
    return 0


def angle_sort(a):
    # 正のx軸から反時計回りにソート
    # 原点は除く
    from functools import cmp_to_key
    return sorted(a, key=cmp_to_key(angle_cross))


class S:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, q):
        hp = 0 if (self.y > 0 or (self.y == 0 and self.x > 0)) else 1
        hq = 0 if (q.y > 0 or (q.y == 0 and q.x > 0)) else 1
        if hp != hq: return hp < hq
        cross = self.x * q.y - self.y * q.x
        return cross > 0

    def __repr__(self):
        return f"({self.x}, {self.y})"


if __name__ == "__main__":
    print(angle_sort([(1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]))
    print(sorted([S(1, -1), S(0, -1), S(-1, -1), S(-1, 0), S(-1, 1), S(0, 1), S(1, 1), S(1, 0)]))
