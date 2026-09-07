- `x.foo` x is null ?
  - 毎回チェックするにはオーバーヘッドが大きい
  - => C などでは「**未定義**」として、その回避を言語処理系の責任ではなくてプログラマーの責任とした
  - => 実行速度的には + だが、バグの原因にもなった
  - 未定義動作に対して**何が起こるかは全く保証されない**
    - nasal demons
- 型安全性
  - **型検査器が ok といったプログラムは、定義されてない状態に陥らない**
  - Meta-Language では意識されてる
    - Ocaml, Haskell
- TypeScript
  - JavaScript にあと付けで型システムを導入する、という出自
  - JavaScript では細かく実行時検査が走る
    - => 未定義動作 はない！
    - **つまり, TypeScript では型安全性が最初から保証されている**
- 型検査器
  - プログラムを解析するプログラム
- 構文木
  - 言語処理系や型検査器を作る人が自由に決めて良い
- ts
  - narrowing
    - https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- 登場人物
  - 対象言語の項の型
  - 型検査器における内部表現

```
const f = (x: number) => x
f(1) <= ok
f(true) <= ng
```

- 引数
  - 実引数: args
  - 仮引数: params
- 変数が現在どういう型を持っているか
  - 型付け文脈, 型環境
  - 変数名 => 型 への対応関係
- 逐次実行
- 部分型付け: subtyping
  - 型Bが型Aの部分型である
    - = 型Aを受け取る関数に型Bの値を渡しても大丈夫
- 再帰型
  - 自分自身を子供にもつ型
- ジェネリクス
  - 型変数
    - ダミーの型
  - 型適応

``` ts
const select = <T>(cond: boolean, a: T, b: T) => (cond ? a : b);

// 型適応 => 関数呼び出し
select<number>(true, 1, 2)
```

- 項と型
- 変数捕獲

