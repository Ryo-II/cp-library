def next_permutation(p):
    n = len(p)
    for i in range(n-2, -1, -1):
        if p[i] >= p[i + 1]:
            continue
        for j in range(n - 1, i, -1):
            if p[i] >= p[j]:
                continue
            p[i], p[j] = p[j], p[i]
            for k in range((n - i - 1) // 2):
                p[i + 1 + k], p[n - k - 1] = p[n - k - 1], p[i + 1 + k]
            return True
    return False


a = [*range(3)]
while 1:
    print(a)
    if not next_permutation(a): break
