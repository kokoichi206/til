## なんでも


## フィルタ

- 入力を、**流れてくるデータ**と捉えている！
  - フィルタは**ストリームを処理する**プログラムともいう！
  - 処理すべき対象をまとまったものとして考えるのではない！
- なんかの例
  - コーフィーフィルタ
  - 空気清浄機日焼け止め

## ドメイン駆動設計

### クリーンアーキテクチャ

- 設計原則
  - この2つ
    - 関心を分離すること
    - 分離した構成要素の依存関係を単純にすること！
  - ↑ からシンプルな円形の図ができる
  - 関心の分離を徹底するには DTO を各層で定義する感じになるな〜
  - クリーンアーキテクチャでの、業務ロジックの自然な置き場所は「エンティティ」になる！

### ドメインモデル

- 目的？
  - 業務知識の整理
  - 関係者が意図を伝える時の基本語彙
- 成長させるには
  - 業務知識を広げ、理解を深める
  - 同じ言葉で開発を進めるための語彙を充実させる
  - プログラミング言語を使った複雑な業務ロジックの表現を改善する
- チームでドメインの知識を共有する
  - チームメンバーが顧客業務に興味を持つようにする
  - ドメインモデルの成長とともにメンバーを育てる

### マイクロサービス

- ドメイン駆動設計の『境界付けられたコンテキスト』の考え方が、分散アーキテクチャの考え方と親和性が高い
- 境界づけられたコンテキスト
  - 言葉の意味が同じになる範囲を、別の意味になる範囲から切り分ける

### ドメインモデル

- ドメイン
  - 知識、影響、活動の領域
- モデル
  - 簡略化！
  - 関連した課題を解決するための簡略化！
- ドメインモデル
  - ルールが適応される限られた範囲を、簡略化したもの

## ログ

- Linux 環境でのログシステム
  - syslog
    - RFC3164
      - https://tex2e.github.io/rfc-translater/html/rfc3164.html
    - ファシリティ: メッセージの種類
    - 重大度

### 設計の基本

- ログとは、「システムのその時の状況を読み手に伝えるための記録」
- まず確認すること
  - ログの用途は何か
  - ログの読者は誰か
  - 満たすべき要件はないかb

## 画像生成 AI

- 生成 AI
- Transformer の登場以降, NN のスケーリング則といったものが知られるようになった
  - 大規模言語モデルのはじまり

## Go らしさ

- Go は Google の問題を解決するために作られた
  - 大規模ソフトウェア開発のため
- 大規模開発時の課題
  - ビルドが遅い
  - 依存性の管理が難しい
  - プログラマーによって言語の習熟度が異なる
    - 可読性
    - ドキュメントの質
  - 同じような開発作業を何度も繰り返してしまう
  - メンテナンスコストが高い
  - バージョンごとに挙動が異なる
- 上の辛さは、端的に言うと**『スケーラビリティの欠如』に起因**している！
- **明確で過不足がないこと（clear and precise）**がシンプルさの所以
- 「書くことが楽しいか？」と「保守が楽か？」はトレードオフの関係だ
  - Rob Pike さん
- 例えば、python で map と for 文を使った時に内部でどのような違いが出るかわかるか？
  - シンプルさとはそういうところ
  - コンパイル後の段階まで含めてのシンプルさ！
- 1つのことを実現するのに、表現方法は少ければ少ないほどいい、ってのが Go の考え方
- 過不足のない？とは
  - スケーラビリティを確保した、優れたプログラムを書くために必要、なもの
- 未使用インポートの不許可
  - 不要なコードをコンパイラ読むことによって、ビルドが遅くなるのを防ぐ
- 未使用変数の不許可
  - 可読性の担保、バグの防止

## zsh, bash

``` sh
memo() {
    local MEMO_DIR="$HOME/memo"
    mkdir -p "$MEMO_DIR"
    local TODAY="$(date +%Y%m%d)"
    vim "$MEMO_DIR/$TODAY.md"
}

PROMPT_COMMAND="echo hello"

curl -o ~/.github-prompt.sh https://raw.githubsercontent.com/git/git/master/contrib/completion/git-prompt.sh

source ~/.github-prompt.sh
PROMPT_COMMAND='__git_ps1 "[\u@\h \t \w" "]\\\$ "'
```

zsh

```sh
precmd() { echo hello }

curl -o ~/.github-prompt.sh https://raw.githubsercontent.com/git/git/master/contrib/completion/git-prompt.sh

source ~/.github-prompt.sh
precmd() { __git_ps1 "[%n@%m %* %~]" "]%(!.#.\$) " }
```

### fzf

``` sh
# mac
brew install fzf

# ubuntu
sudo apt install fzf
```

usage

```sh
cat /etc/shells | fzf

# これえぐ！
git branch --all --format="%(refname:short)" | fzf | xargs git checkout

# git sw でできる！
# えぐ！
git config --global alias.sw '!git branch --all --format="%(refname:short)" | fzf | xargs git checkout'


# bash
select-history() {
    # Write to command-line.
    READLINE_LINE="$(HISTTIMEFORMAT='' history | awk '{print $2}' | fzf --query "$READLINE_LINE")"
    # Move cursor to the right end of the command-line.
    READLINE_POINT=$#READLINE_LINE　
}
# Assign Ctrl + R.
bind -x '"\C-r": select-history'

# これえぐ！
# zsh
select-history() {
    # コマンドラインへ書き込む
    BUFFER="$(history -n -r 1 | fzf --query "$BUFFER")"
    CURSOR="$#BUFFER"
}
# Ctrl + R を割り当てる
zle -N select-history
bindkey '^r' select-history
```

## DynamoDB

- NoSQL
  - Not only SQL
- RDB の特徴
  - リレーショナルモデルによるモデリング
  - **SQL による柔軟な問い合わせ**
  - ACID による厳密なトランザクション
- DynamoDB
  - **より少ないテーブルに収める**ことがベストプラクティス！
    - １アプリケーション１テーブルで構成可能なはずよ
  - Scan は効率が悪いので、なるべく使わないように
