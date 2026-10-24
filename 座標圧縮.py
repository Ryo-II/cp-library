# Coordinate Compression
def cc(a):
    cs = sorted(set(a))
    cd = {v: i for i, v in enumerate(cs)}
    return [cd[ai] for ai in a]


if __name__ == '__main__':
    l1 = [10, 20, 5, 2000, 314, 1414, 27]
    print(cc(l1))
