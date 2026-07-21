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

### 関手: Functor

- 関手（かんしゅ）
- 圏自体も、数学的対象になる
  - 圏C -> 圏D
    - 関手
      - 射とは別のもの
- def
  - 圏 C,D の関手 F とは、次の2つの対応からなる
    - F: ob(C) -> ob(D)
      - X |-> F(X)
    - F: C(X, Y) -> D(F(X), F(Y))
      - f |-> F(f)
  - そして次の2つの条件を満たす
    - identity の保存
      - 1x |-> F(1X) これが恒等射担っててほしい
      - F(1x) = 1F(X)
        - 構造を保っている
    - 合成の保存
      - F(g ∘ f) = F(g) ∘ F(f)
        - 構造を保っている

### 自然変換: natural transformation

- 圏は関手が欲しくて定義してる
- 関手は自然変換が欲しくて定義してる
- 圏の圏 Cat
  - 集合の圏 Set
  - 大きい圏があって圏が複数入ってる
- 関手
  - 恒等変換
  - 圏から圏への関手は複数 F,G 等ある
    - 看守から関手への矢印が自然変換
    - 圏Dにおける射の集まりを自然変換α
- def
  - 登場人物
    - f: X -> Y (C の射)
    - F: C -> D (関手)
    - α: F => G (自然変換)
      - α_x を α の成分 (component) と呼ぶ
  - 関手 F,G: C->D に対する自然変換 α: F=>G とは ∀ X ∈ ob(C) に対して D の射 α_X: F(X) -> G(X) の族（集まり） `(α_X)_{X ∈ ob(C)}` であり、次の条件を満たす
    - α_Y ∘ F(f) = G(f) ∘ α_X
      - f: X -> Y (C の射)
      - F(f): F(X) -> F(Y) (D の射)
      - G(f): G(X) -> G(Y) (D の射)
      - α_X: F(X) -> G(X) (D の射)
      - α_Y: F(Y) -> G(Y) (D の射)
- 可換である
  - 全経路で同じものにたどり着く

### モナド

- 副作用を純粋関数の世界で扱う
  - impure, pure
  - Shall I be pure or impure?
- 不純
  - 標準出力への書き込み、db への書き込み、ファイルへの書き込み、ネットワーク通信、インスタンスの値の変更
- ts, haskell
  - console.log: 
    - hello: Str -> Str
      - 不純
  - Haskell:
    - hello :: String -> IO String
      - **純粋**
    - IO: 計算
      - **作用を及ぼして Str を返す**
      - **計画**の段階でしかないので、純粋、と言い張ってる
      - IO モナド
    - 型構築子: Type Constructor
    - 困りごと
      - IO で包んだはいいけど、中身を使うために繋げられない
      - bind operator (>>=) で繋げる
        - IO a -> (a -> IO b) -> IO b
        - IO a の中身を取り出して、a を使って、IO b を返す関数に渡す
        - bind 演算子も、モナドの一部
- モナドは関手である必要がある
  - 関手
    - IO, [], Mabye, etc
      - 型構築子
      - 共通の振る舞い
        - 型クラス (インターフェースみたいなもの)

```
-- m => IO などにインスタンス化される
-- return の部分は自然変換
class Monad m where
  return :: a -> m a
  (>>=) :: m a -> (a -> m b) -> m b
```

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

### 関手

- 圏C Int -f-> Bool
- 圏D [Int] -F(f)-> [Bool]
  - F(X) = [X]
  - 関数もデータ、
    - F(f) = ? map が良さそう
    - F(f) = map(f)
- Haskell
  - map f arr
  - map :: (a -> b) -> [a] -> [b]
    - 1つの関数を受け取って1つの関数を返す
      - 圏C の関数を圏D の関数に変換する

```
(F(f))(arr: [Int]) -> [Bool] {
  arr.map(x => f(x))
}
```

- Haskell の Fanctor
  - IO
  - Maybe
  - `[]`
  - 型構築子
  - Type Constructor
- Type class
  - インタフェース

``` haskell
-- interface
class Functor f where
  fmap :: (a -> b) -> fa -> fb

-- impl
instance Functor [] where
  fmap = map
```

### 自然変換

- 型の圏
  - Int -f-> Bool
- 別の型の圏
  - 1_type: Int -f-> Bool
  - 2_type: [Int] -F(f)-> [Bool]
    - F ([], map)
  - η_int: Int -> [Int]
    - η_int(x) = [x]
- 可換であること
