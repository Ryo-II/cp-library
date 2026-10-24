"""
n 個の整数からいくつか選んだ時 a にすることができるか
"""


def can_to_a_bfs(n, array, a):  # 未テスト
    from collections import deque
    dq = deque()
    dq.append([0, []])
    while dq:
        qw, used = dq.popleft()

        for i in range(used[-1] + 1, n):
            if i in used or qw + array[i] > a:
                continue
            if qw + array[i] == a:
                return True
            dq.append([qw + array[i], used + [i]])
    return False


def can_to_a_dp(n, array, a):
    dp = [[False] * (a + 1) for _ in range(n + 1)]
    dp[0][0] = True

    for i in range(n):
        for j in range(a + 1):
            dp[i + 1][j] |= dp[i][j]
            if j >= array[i]:
                dp[i + 1][j] |= dp[i][j - array[i]]

    return dp[n][a]


def can_to_a_dp2(n, arr, a):
    dp = [False] * (a + 1)
    dp[0] = True
    for i in range(n):
        for j in range(a, arr[i] - 1, -1):
            dp[j] |= dp[j - arr[i]]
    return dp[a]
