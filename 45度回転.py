# 45度回転して√2倍したもの
# (x, y) なら右回転
# (y, x) なら左回転
def rotate(a):
    return a[1] + a[0], a[1] - a[0]


print(rotate((2, 7)))

"""
使用例
https://atcoder.jp/contests/abc178/tasks/abc178_e
https://atcoder.jp/contests/abc351/tasks/abc351_e
"""
