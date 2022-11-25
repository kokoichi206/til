# Bash スクリプトでよく使うテクニックまとめ

コマンド単位の使い方ではなく、作業効率化のためのスクリプトを書く際などに使えるテクニックをまとめてみました。

便利なものがあれば随時追加していきます。

[目次]

[:contents]

## エラー対策

使用例

- ほとんどのケースでつけておいて損がないエラー対策です

使用コマンド

- set
  - [Set Builtin](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#The-Set-Builtin)
  - `set -e`
    - エラー発生時にスクリプトを終了する
  - `set -u`
    - 未定義の変数を参照時にエラー終了する

```sh
#!/bin/bash
set -eu
```

## ファイル内容のコメント

コメントアウトは `#` で行います。

個人的に、以下のようにファイルの目的・使用方法をファイルの先頭に書くようにしています。

```sh
#!/bin/bash
#
# Description
#    Update CURRENT_PROJECT_VERSION if needed
#
# Usage:
#    bash version_update.sh
#
```

### 複数行のコメント

何もしないコマンド `:` に、ヒアドキュメントを与えてあげます。

```sh
: << '#COMMENT'
例えば、ここに書いた内容が全部コメントになる。
複数行にわたるコメントをかけるだけでなく、
set -x による実行デバッグにおいも呼び出される。
#COMMENT
```

## オプション引数をパースする

使用コマンド

- 「全ての引数」を表す特殊変数`$@`をループで処理しています

注意点

- `-n 2`などのように『オプション + 値』を取るような場合は注意が必要です

```sh
# ======================
# parse arguments (options)
# ======================
for i in "$@"; do
    case $i in
    -h | --help | -help)
        usage_and_exit 0
        ;;
    -s | --slide)
        is_slide=true
        shift 1
        ;;
    -o | --output)
        if [[ -z "$2" ]]; then
            echo "option requires a file name -- $1"
            usage_and_exit 1
        fi
        OUTPUT_PATH="$2"
        shift 2
        ;;
    -*)
        echo "Unknown option $1"
        usage_and_exit 1
        ;;
    *)
        // 何も指定がなければファイル名として解釈したい場合
        if [[ -n "$1" ]] && [[ -f "$1" ]]; then
            FILE="$1"
            shift 1
        fi
        ;;
    esac
done
```

## カスタマイズされたエラーメッセージ

使用例

- 一部分だけ赤文字にしたエラーメッセージを表示します

```sh
# ===== print error =====
function print_error() {
    ERROR='\033[1;31m'
    NORMAL='\033[0m'
    echo -e "${ERROR}ERROR${NORMAL}: $1"
}

# 使用例
if [ ! -f "$FILE" ]; then
    print_error "File $FILE doesn't exist"
fi
```

## ファイル終了時に後処理を行う

使用例

- 途中で処理が失敗したら、事前に作成しておいたバックアップファイルからの復元を行う

使用コマンド

- trap

注意点

- エラーが起こりうる行よりも前に trap を呼ぶ

```sh
// ファイル終了時に呼び出したい関数を定義する
function recover_from_backup() {
    EXIT_CODE="$?"
    // 終了コードが 0 より大きい場合、エラー終了したことを意味する
    if [[ "$EXIT_CODE" -gt 0 ]]; then
        echo "Something went wrong."
        echo "recovered from backup"
    else
        echo "Exit correctly"
    fi
}
# ERR is special feature to bash
trap recover_from_backup EXIT
```

## help を表示する

使用例

- コマンドの使い方及び`-h`オプションを渡されたときの出力例です

```sh
PROGRAM=$(basename "$0")"

# ===== print usage =====
function print_usage() {
    echo "Usage: $PROGRAM [OPTION] FILE"
    echo "  -h, --help, -help"
    echo "      print manual"
    echo "  -o <filename>, --output <filename>"
    echo "      output filename"
}
```

## help を表示して終了：ただし終了ステータスを変えたい

使用例

- コマンドの使用方法（help）を表示 + 実行終了を行いたいが、終了コードを使い分けたい
  - `--help`オプションに対しては 0（正常終了）
  - ファイルが存在しない等のエラーに対しては 1（異常終了）

```sh
usage_and_exit()
{
    print_usage
    exit "$1"
}

# オプションの -h に対する使用例
usage_and_exit 0

# エラー時の使用例
usage_and_exit 1
```

## 特定のファイルに対して１行ごとに処理を行う

```sh
while read -r line
do
    echo "$line"
done < "$FILE"
```

## 変数が正規表現に一致してるかチェック

注意点

- `[`が２つの方法
- `=~`で比較する

```sh
if [[ "$line" =~ ^\`\`\`.* ]]; then
    echo "Code block start (or end)"
fi
```

## sudo 権限でリダイレクトを行いたい

`sh -c` で全コマンドまとめて `sudo` 実行してやるか、`tee` を使ってうまく回避します。

`tee` は確認しつつファイルにも書き込みできてるので便利かと思います。

```sh
# Psermissioin denied
$ echo hoge > /var/www/html/permissio_test
bash: /var/www/html/permissio_test: Permission denied
# echo の前に sudo をつけるが失敗する
$ sudo echo hoge > /var/www/html/permission_test
bash: /var/www/html/permission_test: Permission denied

# `sh -c` を用いてコマンドの引数、リダイレクト含めて指定
$ sudo sh -c "echo hoge > /var/www/html/permission_test"
# 標準出力とファイル出力に同時に出力するteeにsudoをつけて実行
$ echo hoge | sudo tee /var/www/html/permission_test
hoge
```

## おわりに

スクリプトで効率化する時はテンプレに沿うケースが多いと思って、自分がよく使うものをまとめてみました。  
何か一つでも良いと思っていただけたら嬉しいです。
