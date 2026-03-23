## プロパティ

- ステートレスプロパティ
  - 独立していて状態をもたず、副作用がないコンポーネントの検証
- ステートフルプロパティ
- モデル化
  - 非常に単純な実装をモデルとして書く
  - 自明に正しいモデルにする必要がある
  - **神託(oracle)**
    - 参照実装
    - 別のプログラミング言語やソフトウェアパッケージが、『すでに実装されたモデル』として神託として利用できるケースがある
  - **同じプログラムを何種類もかけて、そのうち1つが自明に正しいほど単純な実装になる場合**
  - 問題空間に対する深い理解が求められる
- **事例テストを汎化する**
- 不変条件(invariant)
  - 常に真になるはず、という条件や事実
- **対象プロパティ**
  - symmetric property
  - **変化する部分を全て一度にテストできる**

## ジェネレーター

``` sh
rebar3 as test shell

1> proper_types:term().


2> proper_gen:pick(proper_types:number()).
{ok,5.46920931682217}
3> proper_gen:pick(proper_types:number()).
{ok,-6}
4> proper_gen:pick(proper_types:number()).
{ok,-18.657632290352147}
5> proper_gen:pick(proper_types:number()).
{ok,-2}
6> proper_gen:pick(proper_types:number()).
{ok,-3}
7> proper_gen:pick(proper_types:number()).
{ok,-1}
8> proper_gen:pick(proper_types:number()).
{ok,-15.569737108170331}
9> proper_gen:pick(proper_types:term()).
{ok,2}
```

- 組み合わせ可能な単なる関数
