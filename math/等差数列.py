# 項数 / 2 * (初項 + 末項)
# 項数 / 2 * (初項 * 2 + (項数 - 1) * 公差)

# 初項 a, 末項 b, 項数 n
def sm(a, b, n):
    return n * (a + b) // 2

# 初項 a, 公差 d, 項数 n
def sm(a, d, n):
    return n * (a * 2 + (n - 1) * d) // 2

# 初項 a, 公差 d, 項数 n
def last(a, d, n):  # 末項を求める
    return a + (n - 1) * d
