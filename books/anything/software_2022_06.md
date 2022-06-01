## 何でも

### OpenSSFスコアカード
- セキュリティスコア
- Github リポジトリに対するセキュリティチェック
- Github Actions の workflow


## Shell

### sec 1
- GUI: Graphical User Interface
    - GUI でも「グラフィカルシェル」を介してカーネルに情報が伝わっている
- CUI: Character-based User Interface
- シェル
    - カーネルとの間の仲介役

``` sh
echo $PS1

# 2,1 はファイルディスクリプタ番号
cat /proc/cpuinfo >> ~/cpuinfo.txt 2>&1
# 標準入力としてファイルを利用する！
sort < ~/cpuinfo.txt
# どちらも同じ結果になる！ほう。
sort < ~/cpuinfo.txt > ~/cpuinfo_out.txt
sort > ~/cpuinfo_out.txt < ~/cpuinfo.txt
```

- オプション
    - ロングネームオプション
    - ショートネームオプション
- | は標準出力のみ！
    - 標準エラー出力も渡すには、以下のようにする
    - `cmd1 2>&1 | cmd2`
    - `cmd1 |& cmd2`
- よく使うキーバインド
    - Ctrl + a,e,u
    - これから使っていきたい
        - Ctrl + s,r
        - Esc + b,f

``` sh
ls -CF

# 九九
echo {1..9}\*{1..9} | xargs -n 1 | bc | xargs -I@ printf "%02d\n" @ | xargs -n 9 | sed -E 's/0([0-9])/ \1/g'
```

- チルダプレフィックス

``` sh
for i in *.txt; do cp $i ${i/txt/orig.txt}; done
```

- デフォルト値の使用、代入、別値の使用
    - ${parameter:-word}
        - parameter の値が未設定か空文字列であれば、word を展開したものに置換され、表示される
    - ${parameter:=word}
        - parameter の値が未設定か空文字列であれば、word を展開したものに置換される
        - parameter に word が入ってくる？
- 部分文字列展開
    - ${parameter:offset:length}
- パラメータの長さ
    - ${#parameter}
- 前方一致する変数名
    - ${!prefix*}
    - ${!prefix@}
- 算術式展開
    - $((expression))
- コマンド置換
    - $()
    - ``
- プロセス置換
    - <(command)


### sec 3
- シェルスクリプトの利点
    - 自動化に役立つ
    - 高移植性
    - オペミス防止
- 使うべきでない時  
    - リアルタイム性が要求される時
    - 100行を超えるくらい大きくなる時
- WHY Bash: Bourne Again SHell
    - POSIX モードの存在
        - `--posix (set -o posix)`
- シェバン
    - `#!/bin/sh` は**ほとんどの環境ではシンボリックリンク！**
        - `#!/bin/bash` と明示的にする

``` sh
target=$(ls | grep backup | head -n 1)
# これでは空の変数に対し、${HOME}/ が実行されてしまう！
rm ${HOME}/${target}
# 変数がからの場合にエラー終了する
rm ${HOME}/${target:?}
```

- バイナリ埋め込みインストーラ
    - .deb, .rpm パッケージや tarball などのバイナリをシェルスクリプトの末尾に埋め込み、実行時にバイナリ部分を抽出して、インストール作業を進めることがある
    - 利便性が高い

### dotfiles
dotfiles 作ってみたいかもしれない、次回以降に期待


## AWS の DB 選び！
RDS, DynamoDB


## サイバー脅威インテリジェンス
- ファイルの一意な識別方法
- [VirusTotal](https://www.virustotal.com/gui/home/search)
    - ハッシュ値から怪しいファイルか判別する


## サーバー・運用
- Shadowserver
    - グローバルIPアドレスの脆弱性チェック



