## sec 0

大きく 2 種類

- Attack-Defence
  - 攻防戦型
- Jeopardy
  - 問題出題型

[CTF Time](https://ctftime.org/) に CTF の開催状況がまとまっている。

## sec 1

Pwn(Exploitation) という脆弱性の分野もある。

### Linux コマンド

```sh
$ file

stripped とかなってたらあれ
```

```sh
$ readelf
```

```sh
# ファイル中の表示可能文字列を抽出して表示。
# デフォルトでは4文字以上の連続した文字の並び。
strings file_name
```

```sh
grep
```

```sh
unzip

tar

gunzip

xz
```

トレーサ

```
strace
ltrace
```

デバッガ

```
GDB
OllyDbg <- Windows のバイナリを解析するためのデバッガ
Immunity Debugger
```

逆アセンブラ

```
IDA
objdump
```

バイナリエディタ

```
ghex <- Linux
Vim + xxd
vim -b
-> ":%!xxd"
-> ":%!xxd -r"
```

仮想化ソフトウェア

```
VirtualBox
VMware Player
```

### 動的解析

バイナリを実際に動作されることによって得られる情報から解析する。

### gdb

gdb: Linux の実行形式である ELF ファイルをはじめとして、様々な形式の実行ファイルを解析できるデバッガ。

レジスタ名を指定: `$eax` みたいに、`$` をプレフィックス
メモリアドレスを参照: `*0x8000000` みたいに、`*` をプレフィックス

```sh
$ gdb
$ gdb (デバッギーのファイル名)
$ gdb -p (デバッギーのプロセス ID)

# 逆アセンブルの表示
gdb$ disas (関数名)
gdb$ disas (関数内での開始アドレス) (関数内での終了アドレス)

# 関数に含まれていない領域を逆アセンブル
gdb$ x/ (命令数) i (先頭アドレス)

# gdb ではデフォルトで AT&T 記法 → Intel 記法にする
# うーん、ARM アーキテクチャでは Intel の方にできない？
# https://github.com/pwndbg/pwndbg/issues/27
gdb$ set disassembly-flavor intel
set disassembly-flavor intel

# ブレイクポイント
gdb$ b (関数名)

# できること表示？
(gdb) apropos disassembly

(gdb) disas main
(gdb) b *0x00000000000009b4
(gdb) i b
(gdb) d 1

# ステップ実行
(gdb) r

# main 関数でブレイク
(gdb) start

```

### 静的解析

プロセッサのアーキテクチャによって、どのような命令が用意されているかが変わってくるため、アセンブリ命令を理解するには、プロセッサのアーキテクチャや、プロセッサの用いるデータ構造をよく理解する必要がある！

レジスタとスタック。

レジスタ

- プロセッサ内に存在する記憶装置、メモリや補助記憶装置と比較して高速！
- 32bit, 64bit 程度のもの
  - 32bit CPU, 64bit CPU はこのレジスタ幅から消えている

汎用レジスタは、どんな使い方をしても問題はないが、通例としての使い方が決められている。

- EAX: 演算の結果を格納
- ECX: ループの回数などのカウント
- EDX: 演算に用いるデータ
- EBX: アドレスのベース値
  ...

特殊レジスタには、それぞれ専用の用途がある！

- EBP: 現在のスタックフレームにおける底のアドレス
- ESP: 現在のスタックトップのアドレスを保持
- EIP: 次に実行するアセンブリ命令のアドレス

条件分岐命令との関わりは重要。

- CF: キャリーフラグ
  - 演算命令でキャリー（桁上がり）かボロー（桁借り）が発生した時にセットされる
- ZF: ゼロフラグ
  - 捜査の結果が 0 になった場合にセットされる
- SF: 符号フラグ
  - 捜査の結果が負となった場合にセットされる
- DF: 方向フラグ
  - ストリームの方向を制御する
- OF: オーバーフローフラグ
  - 符号付き算術演算の結果がレジスタの格納可能範囲を超えた場合にセットされる

バイトオーダ

MSB: Most Significant Byte
LSB: Least Significant Byte

16 進数で 01020304 なら、MSB は 01, LSB は 04

ビッグエンディアンなら 01020304
リトルエンディアンなら、04030201

アセンブリ言語には、Intel 記法や AT&T 記法がある。

```
Intel 記法
    mov eax, 5
AT&T 記法
    mov $5, %eax
```

```c
int i;
for (i = 0; i < 5; i++) {
    func();
}
```

と同等のアセンブリの命令

```
    xor ecx, ecx
loc_1:
    call func
    inc ecx
    cmp ecx, 5
    jne loc_1
```

静的リンクと動的リンク。

API 呼び出しを全くしておらず、ユーザ定義の関数のみを呼び出しているバイナリがあるかも、その場合は共有ライブラリのリンクの仕方に原因がある。
良く見るのは動的リンク。動的リンクとは、外部のライブラリファイル（.so, .dll）を、リンカに実行時に動的にリンクすることで、バイナリを実行する方式。一方で静的リンクとは、外部のライブラリファイルをコンパイル時にリンクし、生成する実行ファイルに含めることで、実行時にリンクする必要をなくす方式。

さらに静的リンクかつ stripped なバイナリとでは、非常に大きな差がある。
stripped なバイナリとは、シンボル情報が削除されたバイナリのこと！
→ ユーザ定義関数と標準ライブラリ関数の見分けがつかなくなる。

アセンブリ言語を読んで、アルゴリズムを追いきれない時は紙に書く！

- スタックが push/pop 命令でどのように変化しているか
- レジスタの値はどうなっているか
- 論理演算やビットシフトの計算結果がどのようになるか

### objdump

```sh
objdump -d check_me
objdump -d -M intel a.out

Disassembly of section .fini:

0000000000000a5c <_fini>:
 a5c:   d503201f        nop
 a60:   a9bf7bfd        stp     x29, x30, [sp, #-16]!
 a64:   910003fd        mov     x29, sp
 a68:   a8c17bfd        ldp     x29, x30, [sp], #16
 a6c:   d65f03c0        ret
```

## sec 2

pwn
オンラインゲームで own をタイプミスしたことから生まれ、「勝つ」や「打ち負かす」といった意味のスラングとして定着。

checksec.sh
https://github.com/slimm609/checksec.sh
下調べのステップで行う RELRO, SSP, NX bit の確認に使う

peda
https://github.com/longld/peda
gdb の機能を大幅に強化してくれる拡張スクリプト

socat
リモートエクスプロイトを、手元で再現するときに便利なツール

### 実行ファイルのセキュリティ機構

脆弱性の被害を緩和するために幾つかのセキュリティ機構を付与している。

- RELRO: RELocation ReadOnly
- SSP: Stack Smash Protection
  - gcc で `-fno-stack-protector` で意図的に無効化
  - スタック上でのバッファオーバーフローを防ぐ仕組み
- NX bit: No eXecute bit
  - 必要のないデータを実行不可能に設定
  - gcc では `-z execstack` で無効にできる
- ASLR: Address Space Layout Randomization
  - アドレスの一部をランダム化することでアドレスを推測するのを困難にしている
- PIE: Position Independent Executable
  - 実行コード内のアドレス参照を全て相対アドレスで行うことで、実行ファイルがメモリ上のどの位置に置かれても正常に実行できるようにする

```sh
# OFF
sysctl -w kernel.randomize_va_space=0
> sysctl: setting key "kernel.randomize_va_space", ignoring: Read-only file system

# ON
sysctl -w kernel.randomize_va_space=2
```

```
readelf -s a.out | grep buffer
```

| 領域  | 32bit  | 64bit  |
| :---: | :----: | :----: |
| stack | 11 bit | 20 bit |
| mmap  | 8 bit  | 28 bit |
| heap  | 13 bit | 13 bit |

共有ライブラリは mmap を用いてメモリに配置されるので、32 bit では 8bit -> 256 通りのランダム化しか提供しない！
→ **ASLR の回避方として簡単なのはブルートフォース！**

## sec 3

ネットワークは非常にレイヤーが綺麗に区切られている。
それぞれのレイヤーでは、そのプロトコルに必要な情報を渡されたデータの先頭に付与。
この**付与した情報をヘッダと呼び、この作業をカプセル化**という。

パケットが記録されるファイル

libpcap (Packet capture library)
`.pcap` ファイル。

### Netcat

```sh
nc (接続先 IP アドレス) (接続先ポート番号)
```

## memo

```
localhost
LOcalHost
127.0.0.1
0x7f.0.0.1
2130706433
```

0.0.0.0 をどこにするかは相手のネットワーク次第。

domain 名は、基本大文字小文字区別しない。

破損してる png ファイル。

ajax の callback に値があれば、任意のスクリプトを実行できる。

常設 CTF やるときは、ライトアップとかで調べる。
