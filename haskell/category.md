## 圏: Category

- 抽象度の順
  - 数 -> 集合, 群, 環, 体 -> 圏
- 圏 1945
  - Haskell 1987
  - monad 1992 => Haskell
- 圏
  - 点と点の間の矢印
    - 有向グラフ？
  - X - f -> Y - g -> Z
    - X, Y, Z: 対象 (object)
    - f, g: 射 (morphism, arrow, map)
      - しゃ
    - g ∘ f: 合成 (composition)
      - f いって g いく
      - f: X -> Y, g: Y -> Z
      - g ∘ f: X -> Z
  - X -> X: 自己射
    - 恒等射 (identity morphism)
    - id_X: X -> X
  - 必ず合成は存在する
- def: 圏
  - 次の3つからなり
    - 対象の集まり: ob(C)
    - 任意の対象 X,Y に対して射の集まり: C(X,Y) hom(X,Y)
    - 合成と呼ばれる二項演算: ∘: C(Y,Z) × C(X,Y) -> C(X,Z)
      - (g, f) ↦ g ∘ f : g after f
  - 2つの条件を満たす（公理）
    - identity
      - 任意の対象 X <- ob(C) は 1_X をもち, f ∈ C(X,Y) に対して f ∘ 1_X = f = 1_Y ∘ f
    - associativity: 結合律
      - 任意の対象 X,Y,Z,W <- ob(C) と射 f ∈ C(X,Y), g ∈ C(Y,Z), h ∈ C(Z,W) に対して h ∘ (g ∘ f) = (h ∘ g) ∘ f
- 推移律
- 順序圏
- モノイド
  - 単一対象の圏

## programming?

- 対象
  - 型
- 射
  - 関数
- 条件
  - 1_int,
    - Haskell には id っていうのがある
  - 結合律
    - 外延的に等しい
- どんな関数も圏？
  - 純粋ではなさそう。。？
    - 例外
    - 副作用
    - ランダム
      - タイミングによって同じ input でも異なる
      - 参照透過性がない
  - 引数が複数
    - output として関数（= データとして扱ってる）
    - **first-class function**
    - Haskell も全てカリー化された形で型定義をする必要
- 単純型付きλ計算 = デカルト閉圏
  - 『対象 => 対象』も対象になるのを、閉じてる、という

### λ計算

λx.(λy.x+y) <=> add(x,y){x+y}

first-class function
1つの引数（カリー化）

```
add(x,y){x+y}
add(x){(y) => x+y}
```

関数をデータとして扱う => **関数も型を持つ** => **関数が圏論の対象になる**

これは発見されたもの、他の言語は発明されたもの

**無名関数 = lambda 式**
