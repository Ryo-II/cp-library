from sortedcontainers.sortedset import SortedSet

"""
Mexを取りたいとき
"""

ss = SortedSet(range(100))
for i in range(20):
    ss.discard(i)
print(ss[0])
