from collections import deque

n, x = map(int, input().split())

dp = [[-1] * (x + 1) for _ in range(n + 1)]
dp[0][0] = 0
for i in range(1, n + 1):
    value, weight, count = map(int, input().split())
    for j in range(value):
        dq = deque()
        k = 0
        while j + k * value <= x:
            a = j + k * value
            if dq and k - dq[0] > count:
                dq.popleft()
            while dq and dp[i - 1][j + dq[-1] * value] + (k - dq[-1]) * weight < dp[i - 1][a]:
                dq.pop()
            if dp[i - 1][a] != -1:
                dq.append(k)
            if dq:
                dp[i][k] = dp[i - 1][j + dq[0] * value] + (k - dq[0]) * weight
            k += 1

print(dp[n][x])

"""
value が x 以下で wight を最大化したい
ただし各要素について count 以下の数しか選べない

各 dp[i][j] は j mod value ごとに独立
dp[i][j] = max(dp[i-1][s] + w*t, dp[i-1][s+1] + w*(t-1), ... , dp[i-1][s+k] + w*(t-k))
最後の項が dp[i-1][j] * w*0 である
これをスライド最大値で持つ
"""
