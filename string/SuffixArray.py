# https://mametter.hatenablog.com/entry/20180130/p1

class SuffixArray:
    def __init__(self, string):
        self.s = string
        self.n = len(string)
        if self.n == 1:
            self.arr = [0]
        else:
            self.arr = self.sa_is(tuple(map(lambda c: ord(c) - 96, string)) + (0,), 26 + 1)[1:]

    def is_lms(self, t, i):
        return i > 0 and t[i - 1] == 1 and t[i] == 0

    def induced_sort(self, s, k, t, lmss):
        n = len(s)
        sa = [None] * n

        bucket = [0] * (k + 1)
        for si in s:
            bucket[si + 1] += 1
        for i in range(k):
            bucket[i + 1] += bucket[i]

        bucket_idx_right = [bucket[i + 1] - 1 for i in range(k)]
        for lms in reversed(lmss):
            c = s[lms]
            sa[bucket_idx_right[c]] = lms
            bucket_idx_right[c] -= 1

        bucket_idx_left = bucket[:-1]
        for i in sa:
            if i is not None and i > 0 and t[i - 1] == 1:
                c = s[i - 1]
                sa[bucket_idx_left[c]] = i - 1
                bucket_idx_left[c] += 1

        bucket_idx_right = [bucket[i + 1] - 1 for i in range(k)]
        for i in reversed(sa):
            if i is not None and i > 0 and t[i - 1] == 0:
                c = s[i - 1]
                sa[bucket_idx_right[c]] = i - 1
                bucket_idx_right[c] -= 1

        return sa

    def sa_is(self, s, k):
        n = len(s)

        # S型(0): s[i] < s[i+1]
        # L型(1): s[i] > s[i + 1]
        # 末尾はS型
        # s[i] == s[i + 1] なら s[i + 1] と同型
        t = [None] * n
        t[-1] = 0
        for i in range(n - 2, -1, -1):
            if s[i] < s[i + 1]:
                t[i] = 0
            elif s[i] > s[i + 1]:
                t[i] = 1
            else:
                t[i] = t[i + 1]

        lmss = [i for i in range(n) if self.is_lms(t, i)]
        seed = lmss
        sa = self.induced_sort(s, k, t, seed)
        sa = [i for i in sa if self.is_lms(t, i)]

        nums = [None] * n
        nums[sa[0]] = num = 0
        for idx in range(len(sa) - 1):
            i, j = sa[idx], sa[idx + 1]
            diff = False
            d = 0
            while True:
                i_d = self.is_lms(t, i + d)
                j_d = self.is_lms(t, j + d)
                if s[i + d] != s[j + d] or i_d != j_d:
                    diff = True
                    break
                elif d > 0 and (i_d or j_d):
                    break
                d += 1
            num += diff
            nums[j] = num
        nums = [num for num in nums if num is not None]

        if num + 1 < len(nums):
            sa = self.sa_is(nums, num + 1)
        else:
            sa = [None] * len(nums)
            for i, c in enumerate(nums):
                sa[c] = i

        seed = [lmss[i] for i in sa]
        sa = self.induced_sort(s, k, t, seed)

        return sa

    def print_arr(self):
        for i in range(self.n):
            print(i, self.s[self.arr[i]:])

    def op(self, s, t, i=0):
        # i-1 文字目まで一致済み
        while s + i < self.n and i < len(t):
            if self.s[s + i] != t[i]:
                break
            i += 1
        if i == len(t):
            return i, 0
        if s + i == self.n:
            return i, -1
        return i, ord(self.s[s + i]) - ord(t[i])

    def _bisect(self, t, funk=lambda x: x >= 0):
        l, r = -1, self.n
        l_idx = 0
        r_idx = 0
        while l + 1 < r:
            mid = (l + r) // 2
            ni, f = self.op(self.arr[mid], t, min(l_idx, r_idx))
            if funk(f):
                r = mid
                r_idx = ni
            else:
                l = mid
                l_idx = ni
        return r

    def bisect_left(self, t):
        return self._bisect(t)

    def bisect_right(self, t):
        return self._bisect(t, lambda x: x > 0)

    def count(self, t):
        return self.bisect_right(t) - self.bisect_left(t)

sa = SuffixArray("banana")
sa.print_arr()
print(sa.count("banan"))
