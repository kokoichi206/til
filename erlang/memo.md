## Erlang, Elixir

- Erlang
  - 言語 + **VM（BEAM）** + 標準ライブラリ
  - 並列・分散・耐障害性に特化
  - OTP（フレームワーク）が本体レベルで強い
  - beam => binary file
- Elixir
  - Erlang VM（BEAM）上で動く言語
  - 文法は Ruby っぽくて書きやすい
  - Erlang の資産（OTP, ライブラリ）をそのまま使える
- Erlang
  - Process Isolation
    - Fault Tolerance
    - **let it fail**
  - Concurrency model
  - **No type but specs**
    - dynamic typing
  - Any green threads..?
- Erlang/OTP
  - 高可用性、並行性、耐障害性に優れたリアルタイムシステム向けに設計されたプログラミング言語Erlangと、その設計パターン（ライブラリ）であるOTP（Open Telecom Platform）を統合した環境

## 環境確認

``` sh
# Erlang のバージョン確認
erl -eval 'erlang:display(erlang:system_info(otp_release)), halt().'

# Elixir のバージョン確認
elixir --version

# 対話シェルが起動するか
iex
```

``` sh
5> cd("/Users/kokoichi206/ghq/github.com/kokoichi206/til/erlang/hello").
/Users/kokoichi206/ghq/github.com/kokoichi206/til/erlang/hello
ok
6> c(main).
main.erl:4:1: syntax error before: main
%    4| main() ->
%

8> c(main).
{ok,main}
9> main:main().
Hello, World
ok
10>
~
```

``` erlang
cd("/Users/kokoichi206/ghq/github.com/kokoichi206/til/erlang/chat").

c(pastebeam).

Pid = pastebeam:start().

f() ->
  expr1,
  expr2,
  expr3.

% loop や for 文はないので。
pastebeam:loop(10).
10
9
8
7
6
5
4
3
2
1
ok
13>
```

``` sh
telnet localhost 5016
```

```
13,10 => \r\n
```
