## プロパティ

- ステートレスプロパティ
  - 独立していて状態をもたず、副作用がないコンポーネントの検証
- ステートフルプロパティ

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
