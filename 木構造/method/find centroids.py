n = 10
g = [[] for _ in range(n)]
e = [(i, i + 1) for i in range(n - 1)]
for i in range(n - 1):
    u, v = e[i]
    g[u].append(v)
    g[v].append(u)
w = [1] * n
sw = sum(w)

centroids = []
sub_w = [0] * n


# 木の重心を求める
def find_centroids(u, p=-1):
    sub_w[u] = w[u]
    is_centroid = True
    for v in g[u]:
        if v == p:
            continue
        find_centroids(v, u)
        if sub_w[v] > sw / 2:
            is_centroid = False
        sub_w[u] += sub_w[v]
    if n - sub_w[u] > sw / 2:
        is_centroid = False
    if is_centroid:
        centroids.append(u)


find_centroids(0)
print(centroids)
