"""
平均値を最大化したい

例: A=[a1, a2, ... , aN] で sum(A[i] (i∈S))/|S| を最大化したいとき
### 選ぶ集合に対して追加の制約があるとき

# 愚直解
ans = 0
for S in range(1 << N):
    if (Sが条件を満たさない): continue
    sm = 0
    for i in range(N):
        if S >> i & 1:
            sm += A[i]
    ans = max(ans, sm)


# 二分探索
# 「x以上にできるか？」
k = |S|
sum(A[i]) / k >= x
sum(A[i]) >= kx  # 両辺にkをかけただけ
sum(A[i] - x) >= 0  # ちょっと不思議だが、k個のxをk回に分けて引いてるだけ。
# 「ある集合の和が0以上か？」という問題になる


勝率も特殊な場合の平均値である
"""