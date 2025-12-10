## What is Zig?

- C の後継を目指す
- 原則
  - No hidden control flow
    - 演算子オーバーロードなし
      - `a + b` が想定外の動きをする
    - 例外なし
    - デストラクタなし
      - defer
    - 明示的
  - Explicit allocators
    - メモリ割り当てを明示
  - Compile-time code execution
    - コンパイル時コード実行
- impl
  - error union (!T)
    - Result
  - ?T
    - Option
  - comptime
    - トレイト
- シンプルさと制御を重視
- 配列とスライス
- 組み込み関数
  - https://ziglang.org/documentation/master/#Builtin-Functions

## command

``` sh
zig run hello.zig

zig build
zig build run


zig test hello.zig
```
