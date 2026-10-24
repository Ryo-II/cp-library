# 部分集合の列挙
n = 10

# 通常
ans1 = 0
for bit1 in range(1 << n):
    for bit2 in range(1, 1 << n):
        if bit1 & bit2 == bit2:
            ans1 += 1

# 推奨
ans2 = 0
for bit1 in range(1 << n):
    bit2 = bit1
    while bit2:
        ans2 += 1
        bit2 = (bit2 - 1) & bit1

print(ans1)
print(ans2)
