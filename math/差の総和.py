"""
n = size
a = [x1, x2, x3 ... xn]

について

O(n^2)
for i in range(n - 1):
    for j in range(i + 1, n):
        ans += abs(a[j] - a[i])

を求める時

O(n log n) ソート + n
b = sorted(a)
sz = len(b)
for i in range(sz):
    ans += b[i] * (2 * i + 1 - sz)

になる

b[i] * (2 * i + 1 - sz) は
i = ans に b[i] を足す回数
sz - (i + 1) = ans から b[i] を引く回数
である

n = 6 の時、各 i について
 -----
+ ----
++ ---
+++ --
++++ -
+++++
である
"""

# 検証
from random import randint

n = 20
m = 100
l, r = 0, 10 ** 8  # [l, r]

a = [randint(l, r) for _ in range(n)]
cnt = [0] * n
for i in range(n - 1):
    for j in range(i + 1, n):
        cnt[i] -= 1
        cnt[j] += 1
print(cnt)

for _ in range(m):
    a = [randint(l, r) for _ in range(n)]
    ans_a = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            ans_a += abs(a[j] - a[i])

    b = sorted(a)
    ans_b = 0
    sz = len(b)
    for i in range(sz):
        ans_b += b[i] * (2 * i + 1 - sz)

    if ans_a != ans_b:
        print("不一致", ans_a, ans_b)
        break
else:
    print("一致")
