## なんでも

- ドメイン
  - 2023/11 RFC9460
    - https://tex2e.github.io/rfc-translater/html/rfc9460.html
    - → HTTPS という DNS レコードの標準化！
    - パフォーマンスを向上させる目的もある
  - これまで
    - **ハンドシェイク時の ALPN によってサーバーが推奨する接続方法で接続していた**
      - **TLS ハンドシェイク**
    - 接続しようとしてみるまで、どのプロトコルでやり取りするかわからない！
  - HTTPS レコード
    - サーバー側で利用されているプロトコルなどの情報を DNS で提供するようになった！
    - オーバーヘッドを無くし、接続速度を上げることができる
      - さらに
        - 接続先がサポートしている暗号化方式
        - 推奨されてる通信プロトコルのバージョン
        - などを提供可
      - ほんと？
        - https://chatgpt.com/share/6760a27c-c520-8004-8e58-e3883ff0005a
        - 現状では HTTP3 へのメリットが大きい
    - FQDN を登録もできる
      - これまで Route53 の ALIAS レコードのような独自実装でしかなかった
      - ゾーンアペックスでの他 FQDN への転送が、
      - 標準化された仕様で可能になった！
    - Zone APEX
      - サブドメインを持たないドメイン、頂点のこと
  - 意義
    - 特にモバイルで顕著

``` sh
# ALPN のやりとり。
> curl -I -v 'https://example.com/'
* Host example.com:443 was resolved.
* ...
* ALPN: curl offers h2,http/1.1
* ...
* ALPN: server accepted h2
```

- Swift
  - 特徴？
    - nil 安全
    - LLVM コンパイラによって最適化された機械語へと変換
    - **プロトコル指向プログラミング**
      - プロトコルに対する拡張
    - 関数型プログラミングのサポート
  - Python と連携した機械学習フレームワークの試み
  - SwiftUI
  - Swift Concurrency
    - **データ競合安全性への取り組み**
      - **アクターモデル**
      - 原則スレッドをブロックしない
    - Swift6
- Cloudflare Workers
  - Cloudflare Queues
    - メッセージキューイングシステム
    - Queue, Message, Batch
    - DLQ
      - max_retries に達した後に再配信を要求された場合 DLQ に格納される
- QA
  - 初の QA メンバーでやったこと？
    - バグチケットの流れの整理
    - バグの分析
    - MTTR
  - テストケースを notion で管理
    - テストのための仕様一覧をまとめた
    - テストデータを開発環境に投入する仕組み
- Databricks
  - データメッシュ
    - サイロ化されてしまう可能性が高い
    - 本質
      - **組織的なスケーリングに対するパラダイムシフト**
      - **ドメイン主導によるデータオーナシップ**
    - ガバナンスモデル
    - **Data as a Product**
  - データプロダクト
- AWS WAF
  - **インターネットトラフィックのうち、ほぼ半数は bot のアクセス**
    - いい bot
      - 検索エンジンの品質向上
      - Web トラフィックのモニタリング
    - 悪い bot
      - トラフィック全体の 3 割
- ISP
  - インターネットの出入り口
  - ISP の運用ルータ
    - 全世界のネットワークルーティング情報が保持されている
      - フルルート
  - ISP は日本に150社以上ある
    - https://jaipa.or.jp/member/

## 暗号

- 暗号化
  - 共通鍵暗号方式
    - DES 8 byte
    - AES 16, 24, 32 byte
  - 公開鍵暗号方式
    - DH 鍵共有
    - RSA

``` sh
# ============= 共通かぎ暗号方式 =============
# 32 は共通鍵のバイト数。
openssl rand -base64 -out test.key 32

$ openssl enc -aes-256-cbc -in test.txt -out test.enc -pass file:test.key
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.

# ================= 公開鍵暗号方式 =============
openssl genrsa -out rsa-private.key
openssl rsa -in rsa-private.key -pubout -out ras-public.key


```

### デジタル署名

- 署名鍵
  - 実生活の実印にあたるもの
  - **印鑑証明に当たるものが検証鍵によるチェック**
- 鍵の管理・作成は**送信者**

## シェルスクリプト

### とは

- シェル
  - bash
    - Bourne Shell 互換として開発されたもの
    - Bourne Again SHell
    - 多くのディストリビューションのデフォルトシェルとして提供されたため広く普及された
    - POSIX モードにより POSIX 準拠のシェルとしても動作可能
- シェルスクリプトの制約
  - POSIX 準拠
  - 環境の固定化
- **現代の**シェルスクリプトの使われ方
  - いつ適しているか
    - 複雑な処理をしない箇所
      - 使い捨てスクリプト
      - コマンド実行のラッパー
      - バッチ処理のスクリプト
    - 環境の依存を消したい
      - コンテナ
      - IaC
      - CI/CD

### 基本

- リダイレクト・パイプ
  - 標準入力・標準出力・標準エラーはデフォルトでは**端末デバイス**
  - 複数リダイレクトがある場合、左から右へと評価される。。。？

``` sh
# 標準エラーを標準出力に**複製**
cat hoge > pien 2>&1
```

- 後続行の内容をリダイレクト
  - `<<delimiter`
  - いわゆるヒアドキュメント

``` sh
cat <<DOCUMENT
hoge
fuga
piyo
DOCUMENT
```

- コマンド置換
- 算術展開
- **複合コマンド**
  - グルーピング
    - `{}`
      - 現在のシェル環境で複合リストのコマンドを実行
    - `()`
      - サブシェル環境で複合リストのコマンドを実行

``` sh
{
  echo hoge
  echo fuga
} > hoge.txt
```

- 関数
  - `name() compound-command`
    - **compound-command に複合コマンドを記述できる！**
  - 関数内でのローカル変数
    - `local var=value` で宣言されるが**これは拡張機能！**
    - **POSIX にはない！**
- exec
- dot `.`
  - **他のファイルに記述したスクリプトを現在の環境に読み込む**
  - `[ -f ./.env ] && . ./.env`
  - **`/` が含まれていないと環境変数 PATH に従って探索されてしまう！**

### 使い所

- `nsenter`
  - プロセスの ID を指定しつつコマンドのパスを指定すると特定のネームスペースで任意のプログラムを実行できる
  - `util-linux` に含まれるようになってた
  - **『ネットワーク環境だけ』をコンテナのものにしている**
- git alias
  - **『シェルスクリプト』も登録できる！**

``` sh
# ! で外部コマンド呼び出しになる！
git config --global alias.ac '!git-auto-commit'

git add -A
git ac
```

### better prac

- ShellCheck
  - reviewdog aru
  - https://github.com/reviewdog/action-shellcheck
- ShellSpec

## DB

- N+1 はスロークエリログには出てこないねん
- ORM で気づきにくい場合も
  - ログの確認
  - 統計情報の利用
- N+1 の解消
  - IN
  - JOIN
  - 関数
