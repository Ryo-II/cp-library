def solve(n):
    m = int(n ** 0.5)
    ans = 0
    for i in range(1, m + 1):
        ans += i * (n // i - n // (i + 1))
        if n // i <= m: break
        ans += n // i
    return ans


def solve2(n):
    ans = 0
    i = 1
    while i <= n:
        q = n // i
        r = n // q + 1
        ans += q * (r - i)
        i = r
    return ans


def ture_ans(n):
    ans = 0
    for i in range(1, n + 1):
        ans += n // i
    return ans


if __name__ == "__main__":
    for i in range(10000):
        ta = ture_ans(i)
        if solve(i) != ta:
            print(1, i)
            break
        if solve(i) != ta:
            print(2, i)
            break
    else:
        print("complete")
