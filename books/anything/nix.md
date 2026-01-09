## Nix

- 扱うソフトウェアが増えれば当然トラブルも増える
  - => **潤沢なコンピュータリソースを生かして複雑さそのものをコントロールする**
- パッケージ管理ツール
- **ビルドとデプロイのプロセスを『純粋関数』として扱う**
  - 副作用のないクリーンなパッケージ管理
  - 全てのパッケージを暗号学的ハッシュにより一意なパスに格納
  - **システムの変更はアトミック**
- Nix <= "niks"
  - オランダ語で『無』
- 2015: NixOS Foundation
  - オランダの非営利団体
  - 年 2 回の定期リリース
- nixpkgs
  - 10 万件以上のパッケージ！
- 既存のパッケージマネージャ
  - **FHS: Filesystem Hierarchy Standard**
    - ディレクトリに決められた構造で配置
    - => **全てのパッケージが同じグローバルな空間を共有**
- Nix ストア
  - ビルドした成果物の全てを Nix ストアと呼ばれるディレクトリは以下に保存
  - **アーキテクチャさえ同じであれば同じパスを出力する**
- ガベージコレクション
  - `nix store gc`
  - 現在有効なプロファイルなどから参照されていないものを削除
- Nix 言語
  - 純粋関数型
  - 遅延評価
- **利点**
  - SSoT
  - アトミックな更新
  - クリーンな分離
  - システム構成全体のバージョン管理
- **デメリット**
  - 取得難易度
  - **ディスクスペースの管理**
  - エラーメッセージ
    - 遅延評価の影響もある
- **ユースケース**
  - 一時的なコマンド実行と
  - 開発環境
    - 一度だけ使ってみたい、
    - 特定のバージョンの言語を試したい
  - プロジェクト全体の依存関係管理
  - PC 環境全体の宣言的な管理
  - CI/CD パイプラインの改善

## Getting Started

``` sh
> nix --version
nix (Nix) 2.33.0
```

``` sh
nix-shell -p hello
```

## Flakes

- プロジェクトの依存関係を **flake.nix** と **flake.lock** というファイルに明示的に記述
  - => 誰が実行しても全く同じバージョンのパッケージが使われることを保証
  - => 再現性をより高める
- **事実上の標準**だが、実験的な位置付けを抜け切ってないため手動での有効化が必要
- **nix run, nix shell などが利用可能になる！**

```
experimental-features = nix-command flakes
```

- nix-shell
  - 複数のツールが連携するような環境に便利
- nix run
  - 単一のコマンドを試すのに最適

``` sh
nix run nixpkgs#cowsay -- "hello, nix!"
```

## Nix lang

``` sh
nix repl


nix-repl> 1 + 3
4

nix-repl> "hello" + "niex
        > "
"helloniex\n"

nix-repl> add = x: y: x + y

nix-repl> add 5 10
15

nix-repl> [ 1 1 1 ] ++ [ 2 3]
[
  1
  1
  1
  2
  3
]

# デフォルト値
nix-repl> maker = { pname, version ? "1.0" }: "${pname}-${version}"

# 属性セット
nix-repl> maker { pname = "oooo"; }
"oooo-1.0"

nix-repl> let a = 5; b = 105; in a * b
525

nix-repl> let
        > person = { name = "John"; age = 915; };
        > in
        >   "Name: ${person.name}, Age: ${toString person.age}"
"Name: John, Age: 915"

# rec キーワードで自己参照を可能にする
nix-repl> rec {
        >   fullName = firstName + " " + lastName;
        >   firstName = "John";
        >   lastName = "Doe";
        > }
{
  firstName = "John";
  fullName = "John Doe";
  lastName = "Doe";
}

# merge op "//"
# 右側が優先して上書きされる。
nix-repl> { a = 1; b = 2; } // { c = "john"; a= "paon"; }
{
  a = "paon";
  b = 2;
  c = "john";
}

nix-repl> let
        >   name = "my-pkg";
        >   version = "1.0";
        > in
        >   { inherit name version; }
{
  name = "my-pkg";
  version = "1.0";
}

nix-repl> let
        >   profile = {
        >     name = "alice";
        >     age = 25;
        >     country = "japan";
        >   };
        > in
        >   { inherit (profile) name age; }
{
  age = 25;
  name = "alice";
}
```

## 開発環境

- 特定のプロジェクトに必要なソフトウェアパッケージを一時的に提供する
- 隔離されたシェル環境
- **計量さ**
  - **必要なツールの "参照" だけをその場で切り替える**
  - c.f.
    - Docker
      - OS レベルでの仮想化
      - **Nix はシェルの環境変数の操作、特に PATH**

## Flakes

```sh
nix develop
```

```sh
{
    inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

    outputs = { self, nixpkgs }:
        let
            forAllSystems = nixpkgs.lib.genAttrs [
                "x86_64-linux"
                "aarch64-darwin"
            ];
        in
        {
            packages = forAllSystems (system:
                let
                    pkgs = nixpkgs.legacyPackages.${system};
                in
                {
                    default = pkgs.buildGoModule {
                        pname = "myapp";
                        version = "0.1.0";
                        src = "./.";
                        vendorHash = pkgs.lib.fakeHash;
                    };
                });
        };
}
```

## scope

- プロジェクトの要求
- 個人の好み
  - Git, editor
- システムの状態
  - Mac Dock
  - system font

### プロジェクト固有の管理

- devenv
  - **flake.nix** の課題
    - **記述が複雑になりがち**
  - **定型句を抽象化し、本質的な環境定義だけを記述できるツール**
  - **flake.nix をより簡潔に記述するための DSL**
- c.f.
  - asdf, mise
    - 古いバージョンをインストールする際にビルドが転ける可能性
  - Nix
    - 依存関係を完全に管理するため確実にインストール可能
      - あんまりわかってない

``` sh
nix-shell -p devenv
```

``` sh
devenv init
```

``` sh
devenv shell
devenv up
devenv test
```

### 個人ツールの管理

```
nix-shell -p ripgrep

nix profile rollback

~/.nix-profile
```

``` sh
nix profile add nixpkgs#jq

> which -a jq
/opt/homebrew/bin/jq
/Users/kokoichi206/.nix-profile/bin/jq
/opt/homebrew/bin/jq
/usr/bin/jq
```

- nix-shell でためす
- nix profile で数日使う
- 言うようであれば home-manager の設定追加

**home-manager**

- nix profile
  - ツールの命令的な管理が可能だが、設定ファイルは対象外
- devenv
  - プロジェクト固有の環境を管理するが、ユーザ全体の環境は対象外
- home-manager
  - パッケージ、設定ファイル、デーモンを Nix で一元管理


``` sh
nix-channel --add https://github.com/nix-community/home-manager/archive/master.tar.gz home-manager

nix-channel --update

nix-shell '<home-manager>' -A install

```

``` sh
> cat ~/.config/home-manager/home.nix
{ config, pkgs, ... }:

{
  # Home Manager needs a bit of information about you and the paths it should
  # manage.
  home.username = "kokoichi206";
  home.homeDirectory = "/Users/kokoichi206";
  ...
```

``` sh
home-manager switch
```

### macOS システム設定

- nix-darwin
  - システムレベル
  - c.f.
    - home-manager
      - ユーザレベル

## nix-darwin

https://github.com/nix-darwin/nix-darwin/#getting-started
flakes でやってみる

```sh
sudo mkdir -p /etc/nix-darwin
sudo chown $(id -nu):$(id -ng) /etc/nix-darwin
cd /etc/nix-darwin

nix flake init -t nix-darwin/master

sed -i '' "s/simple/$(scutil --get LocalHostName)/" flake.nix


# ref: https://github.com/nix-darwin/nix-darwin/issues/1228?utm_source=chatgpt.com?utm_source=chatgpt.com
sudo -H nix run \
  --extra-experimental-features "nix-command flakes" \
  nix-darwin/master#darwin-rebuild -- switch
```
