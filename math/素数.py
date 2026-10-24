from collections import defaultdict


# 素因数分解
def prime_factorization(n):
    factors = defaultdict(int)

    while n % 2 == 0:
        factors[2] += 1
        n //= 2
    for i in range(3, n + 1, 2):
        if i * i > n:
            break
        while n % i == 0:
            factors[i] += 1
            n //= i
    if n > 2:
        factors[n] = 1

    return factors


# 約数列挙
def find_divisors(factor):
    divisors = []
    pf = list(factor.keys())

    def dfs(div, res):
        if div == len(factor):
            divisors.append(res)
            return
        for i in range(factor[pf[div]] + 1):
            dfs(div + 1, res * (pf[div] ** i))

    dfs(0, 1)
    return sorted(divisors)


# エラトステネスの篩
def eratosthenes(n):
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if primes[i]:
            for j in range(i * i, n + 1, i):
                primes[j] = False
    return [i for i in range(n + 1) if primes[i]]


# 区間篩 m=max(r-l, r**0.5) O(m log log m)
# [l, r) の素数
def segment_sieve(l, r):
    p0 = eratosthenes(int(r ** 0.5))
    d = r - l
    p1 = [True] * d
    for pi in p0:
        for j in range(pi * max(pi, (l + pi - 1) // pi), r, pi):
            p1[j - l] = False
    return [i + l for i in range(d) if p1[i]]


def main():
    n = 110880
    # f = prime_factorization(n)
    # d = find_divisors(f)
    # print(f)
    # print(d)
    print(segment_sieve(2, 20))


if __name__ == "__main__":
    main()
