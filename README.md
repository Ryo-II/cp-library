# Competitive Programming Library

競技プログラミングで使用する Python のライブラリ・アルゴリズム実装をまとめたリポジトリです。

主に AtCoder などの競技プログラミングでの利用を想定しています。

## Contents

### Data Structures

| File | Description |
|---|---|
| [LinkedList.py](LinkedList.py) | 配列と双方向リンクによる連結リスト |
| [WaveletMatrix.py](WaveletMatrix.py) | Wavelet Matrix。区間内の k 番目の値、値の個数、前後の値などを取得 |
| [FunctionalGraph.py](FunctionalGraph.py) | Functional Graph の分解・解析 |

### Graph Algorithms

| File | Description |
|---|---|
| [rerooting.py](rerooting.py) | 全方位木 DP（Rerooting） |
| [maxflow mincut/](maxflow%20mincut/) | 最大流・最小カット関連の実装 |
| [木構造/](木構造/) | 木構造に関するアルゴリズム |

### Mathematics

| File | Description |
|---|---|
| [convolution_ntt.py](convolution_ntt.py) | NTT による畳み込み（mod 998244353） |
| [CanToA.py](CanToA.py) | 整数の部分集合和問題（BFS・DP） |

### Strings

| Directory | Description |
|---|---|
| [string/](string/) | 文字列関連のアルゴリズム |

### Geometry

| File | Description |
|---|---|
| [45度回転.py](45度回転.py) | 座標の45度回転 |
| [InTriangle.py](InTriangle.py) | 点が三角形の内部にあるかの判定 |

### Other Algorithms

| File | Description |
|---|---|
| [Slide-Min.py](Slide-Min.py) | Sliding Window Minimum（スライド最小値） |
| [next_permutation.py](next_permutation.py) | 次の順列の生成 |
| [座標圧縮.py](座標圧縮.py) | 座標圧縮 |

### Notes

| Directory | Description |
|---|---|
| [math/](math/) | 数学関連の実装・メモ |
| [備忘録/](備忘録/) | アルゴリズムや実装に関する備忘録 |

## Usage

各ファイルは基本的に独立した Python 実装です。

必要な実装をコピーして競技プログラミングの提出コードに組み込むことを想定しています。

```python
from FunctionalGraph import FunctionalGraph

g = [1, 2, 0, 2, 3]
fg = FunctionalGraph(g)

print(fg.cycles)
print(fg.dist_to_cycle)
```

実際のインターフェースや引数については、それぞれのファイルを参照してください。

## Environment

- Language: Python 3
- Primary use: Competitive Programming
- Target platform: AtCoder

## Notes

- 実装は競技プログラミングでの利用を目的としています。
- 一部のファイルには動作確認用のコードやサンプルコードが含まれています。
- すべての実装が汎用ライブラリとして完成しているわけではありません。
- 実装の仕様や制約については各ファイルのコード・コメントを参照してください。