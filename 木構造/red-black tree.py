# http://wwwa.pikara.ne.jp/okojisan/rb-tree/index.html
from typing import cast, Any, Generator
from enum import Enum

Color = Enum("Color", ["R", "B"])

class Node:
    def __init__(self, key, x=None, col=Color.R):
        self.col: Color = col
        self.key: Any = key
        self.val: Any = x
        self.l: Node = NONE
        self.r: Node = NONE
        self.size = 1

def update(u: Node) -> None:
    if u is None:
        return
    l, r = u.l, u.r
    u.size = 1
    if l is not None:
        u.size += l.size
    if r is not None:
        u.size += r.size

NONE = cast(Node, None)

def is_B(t: Node) -> bool:
    return t is not None and t.col is Color.B

def is_R(t: Node) -> bool:
    return t is not None and t.col is Color.R

def rotate_l(v: Node) -> Node:
    u = v.r
    u.l, v.r = v, u.l
    update(v)
    update(u)
    return u

def rotate_r(u: Node) -> Node:
    v = u.l
    u.l, v.r = v.r, u
    update(u)
    update(v)
    return v

def rotate_lr(t: Node) -> Node:
    t.l = rotate_l(t.l)
    return rotate_r(t)

def rotate_rl(t: Node) -> Node:
    t.r = rotate_r(t.r)
    return rotate_l(t)

class RBT:
    root: Node
    active: bool

    def __init__(self):
        self.root = NONE
        self.active = False

    def insert(self, key: Any, x: Any =None) -> None:
        self.active = False
        self.root = self._insert(self.root, key, x)
        self.root.col = Color.B

    def _insert(self, t: Node, key: Any, x: Any) -> Node:
        if t is None:
            self.active = True
            return Node(key, x)
        elif key < t.key:
            t.l = self._insert(t.l, key, x)
            update(t)
            return self._balance(t)
        elif key > t.key:
            t.r = self._insert(t.r, key, x)
            update(t)
            return self._balance(t)
        else:
            t.val = x
            update(t)
            return t

    def _balance(self, t: Node) -> Node:
        if not self.active:
            return t
        elif not is_B(t):
            return t
        elif is_R(t.l) and is_R(t.l.l):
            t = rotate_r(t)
            t.l.col = Color.B
        elif is_R(t.l) and is_R(t.l.r):
            t = rotate_lr(t)
            t.l.col = Color.B
        elif is_R(t.r) and is_R(t.r.l):
            t = rotate_rl(t)
            t.r.col = Color.B
        elif is_R(t.r) and is_R(t.r.r):
            t = rotate_l(t)
            t.r.col = Color.B
        else:
            self.active = False
        return t

    def delete(self, key) -> None:
        self.active = False
        self.root = self._delete(self.root, key)

    def _delete(self, t: Node, key: Any) -> Node:
        if t is None: return NONE
        elif key < t.key:
            t.l = self._delete(t.l, key)
            update(t)
            return self._balance_l(t)
        elif key > t.key:
            t.r = self._delete(t.r, key)
            update(t)
            return self._balance_r(t)
        elif t.l is not None:
            t.l, submax = self._delete_max(t.l)
            t.key = submax.key
            t.val = submax.val
            update(t)
            return self._balance_l(t)
        else:
            self.active = t.col is Color.B
            return t.r

    def _delete_max(self, t: Node) -> tuple[Node, Node]:
        if t.r is not None:
            t.r, submax = self._delete_max(t.r)
            update(t)
            return self._balance_r(t), submax
        else:
            self.active = t.col is Color.B
            return t.l, t

    def _balance_l(self, t: Node) -> Node:
        if not self.active:
            return t
        elif is_B(t.r) and is_R(t.r.l):
            rb = t.col
            t = rotate_rl(t)
            t.col = rb
            t.l.col = Color.B
            self.active = False
        elif is_B(t.r) and is_R(t.r.r):
            rb = t.col
            t = rotate_l(t)
            t.col = rb
            t.l.col = Color.B
            t.r.col = Color.B
            self.active = False
        elif is_B(t.r):
            rb = t.col
            t.col = Color.B
            t.r.col = Color.R
            self.active = rb is Color.B
        elif is_R(t.r):
            t = rotate_l(t)
            t.col = Color.B
            t.l.col = Color.R
            t.l = self._balance_l(t.l)
        else:
            raise Exception("(L) This program is buggy")
        return t

    def _balance_r(self, t: Node) -> Node:
        if not self.active:
            return t
        elif is_B(t.l) and is_R(t.l.r):
            rb = t.col
            t = rotate_lr(t)
            t.col = rb
            t.r.col = Color.B
            self.active = False
        elif is_B(t.l) and is_R(t.l.l):
            rb = t.col
            t = rotate_r(t)
            t.col = rb
            t.l.col = Color.B
            t.r.col = Color.B
            self.active = False
        elif is_B(t.l):
            rb = t.col
            t.col = Color.B
            t.l.col = Color.R
            self.active = rb is Color.B
        elif is_R(t.l):
            t = rotate_r(t)
            t.col = Color.B
            t.r.col = Color.R
            t.r = self._balance_r(t.r)
        else:
            raise Exception("(R) This program is buggy")
        return t

    def _sub_tree_max(self, t: Node) -> Node:
        if t is None: return NONE
        while t.r is not None:
            t = t.r
        return t

    def _sub_tree_min(self, t: Node) -> Node:
        if t is None: return NONE
        while t.l is not None:
            t = t.l
        return t

    def max(self) -> Node: return self._sub_tree_max(self.root)
    def min(self) -> Node: return self._sub_tree_min(self.root)

    def bisect_left(self, key: Any) -> Node:
        p = NONE
        t = self.root
        while t is not None:
            if key < t.key:
                p = t
                t = t.l
            elif key > t.key:
                t = t.r
            else:
                return t
        return p

    def bisect_right(self, key: Any) -> Node:
        p = NONE
        t = self.root
        while t is not None:
            if key < t.key:
                p = t
                t = t.l
            else:
                t = t.r
        return p

    def min_k(self, k: int) -> Node:
        """ソートした時の index が k の Node を返す"""
        if k < 0 or len(self) <= k: raise IndexError(f"{self.__class__} index out of range")
        return self._min_k(self.root, k)

    def _min_k(self, t: Node, k: int) -> Node:
        while t is not None:
            if t.l is None:
                if k == 0:
                    return t
                k -= 1
                t = t.r
            elif t.l.size > k:
                t = t.l
            elif t.l.size < k:
                k -= t.l.size + 1
                t = t.r
            else:
                return t
        return NONE

    def member(self, key) -> bool:
        t = self.root
        while t is not None:
            if key < t.key:
                t = t.l
            elif key > t.key:
                t = t.r
            else:
                return True
        return False

    def lookup(self, key) -> Any:
        t = self.root
        while t is not None:
            if key < t.key:
                t = t.l
            elif key > t.key:
                t = t.r
            else:
                return t.val
        return None

    def keys(self) -> Generator:
        for v in self:
            yield v.key

    def values(self) -> Generator:
        for v in self:
            yield v.val

    def items(self) -> Generator:
        for v in self:
            yield v.key, v.val

    def is_empty(self) -> bool: return self.root is None

    def clear(self) -> None: self.root = NONE

    def __contains__(self, key) -> bool: return self.member(key)
    def __getitem__(self, key) -> Any: return self.lookup(key)
    def __setitem__(self, key, x) -> None: self.insert(key, x)
    def __delitem__(self, key) -> None: self.delete(key)
    def __bool__(self) -> bool: return not self.is_empty()
    def __len__(self) -> int: return 0 if self.is_empty() else self.root.size
    def __iter__(self) -> Generator:
        if self.is_empty(): raise StopIteration
        stack = [(self.root, 0)]
        while stack:
            t, lr = stack.pop()
            if lr == 0:
                stack.append((t, 1))
                if t.l is not None:
                    stack.append((t.l, 0))
            else:
                yield t
                if t.r is not None:
                    stack.append((t.r, 0))


from random import shuffle
rbt = RBT()
it = [*range(10)]
shuffle(it)
print(it)
for i in it:
    if i == 5: continue
    rbt.insert(i, i)

def graph(root):
    node = [root]
    while node:
        nex_node = []
        f = False
        g = ""
        for v in node:
            if type(v) == str:
                g += v
                nex_node.append(v)
                continue
            f = True
            if v.l is not None:
                g += " " * v.l.size
                nex_node.append(v.l)
            g += str(v.key)
            nex_node.append(" ")
            if v.r is not None:
                g += " " * v.r.size
                nex_node.append(v.r)
        if not f:
            break
        print(g)
        node = nex_node

graph(rbt.root)
rbt.insert(5)
print("insert:", 5)
graph(rbt.root)
rbt.delete(5)
print("delete:", 5)
graph(rbt.root)

print(rbt.min_k(5).key)
