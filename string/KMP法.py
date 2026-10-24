def kmp(s, t):
    table = [0] * len(t)
    table[0] = -1
    j = -1
    for i in range(len(t) - 1):
        while j >= 0 and t[i] != t[j]:
            j = table[j]
        j += 1
        table[i + 1] = j

    i = j = 0
    while i + j < len(s):
        if s[i + j] == t[j]:
            j += 1
            if j == len(t):
                return i
        else:
            i = i + j - table[j]
            if j > 0:
                j = table[j]
    return -1


def main():
    S, T = "acbadbabcdba", "dba"
    a = kmp(S, T)
    print(a)


if __name__ == '__main__':
    main()
