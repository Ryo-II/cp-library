# スライド最小値
# 配列aの長さkの区間すべてに対して、その区間内の最小値を求める

from collections import deque

n = 5
a = [2, 3, 4, 7, 2]
k = 3

dq = deque()
for i in range(n):
    while dq and dq[-1] >= a[i]:
        dq.pop()
    dq.append(i)
    if dq[0] == i - k:
        dq.popleft()
    if i >= k - 1:
        print(a[dq[0]])
