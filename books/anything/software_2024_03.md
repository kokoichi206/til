## なんでも

- [OpenTofu](https://github.com/opentofu/opentofu)
  - Terraform
    - v1.5 まで
      - Mozilla Public License (MPL) 2.0
    - 2023/8, v1.6~
      - Business Source License (BSL) 1.1
      - これにより**サードパーティ各社は Terraform を使って HashiCorp 社と競合するサービスを提供できなくなった**
  - そこで v1.5 のものをフォークしてオープンソース版を提供する目的で OpenTofu が作られた
- Domain
  - DNS
    - 名前解決
    - IP アドレス以外にも様々な情報が付与できる
  - リソースレコード
    - DNS に登録される情報の対応関係の定義
    - A, AAAA, MX など
  - A レコード
    - FQDN に対してサーバの IPv4 アドレスを紐づけるためのもの
  - AAAA レコード
    - クアッド A
    - IPv6 を扱う
  - **HTTPS レコード**
    - 2020 に定義された！
    - IP アドレスを返却しつ, HTTP/2, 3 などのプロトコル指定が可能
    - こういった情報を**サーバー接続前にブラウザが取得可能**となる
  - MX レコード
  - TXT レコード
    - **『ドメインを所有する人であること』の証明**になる
    - SSL 証明書
    - Google Analytics の認証コード
    - DKIM の公開鍵
    - など
  - CNAME レコード
  - NS レコード
    - サブドメインの権威サーバを別のサーバに委譲
  - そのほか
    - IP Anycast
      - 1つの IP アドレスで複数のサーバへアクセスできる技術
      - IP アドレスは1つでも最寄りのサーバへアクセスできる
- Chromium
  - Chrome の OSS 版
  - Chromium ベースのブラウザ
    - Edge
    - Opera
    - Brave
    - Vivaldi
    - Arc
    - ...
- デプロイフロー
  - リリースが安全で楽であることは開発速度に非常に良い
  - 誰でも、いつでも、簡単かつ安全に、リリースできる
  - E2E テスト
    - Firebase TestLab
    - WebDriver を使った Web の E2E
  - AWS CDK
    - Terraform とかで管理するのとどうメリット・デメリットあるんだろ
      - 宣言的 vs 手続き的、の考えかと思ってる
    - CDK だと、サブネット ID があれば使い、なければ作成して使う、みたいなことができる
      - そもそもインフラって宣言的に書いた方が見通しがいいんじゃないだろうか。。。
- データベースリファクタリング
  - アンチパターン
    - OR の利用
      - インデックスが効かないためパフォーマンスが悪い
      - クエリが複雑になる
    - 部分一致
      - 前方一致 or 後方一致ならインデックスが使える
      - それ以外は無理
  - OR
    - UNION に置き換える
      - `xxx WHERE new = 1 UNION xxx WHERE old = 1;`
      - 初めから UNION を使うのは早すぎる最適化
      - そもそもインデックスが活用できるようにテーブル設計を見直すべき
  - 全文検索
    - 各 RDBMS によって独自にある
    - PostgreSQL
      - 様々な拡張がある
      - `pg_bigm` など
        - **全文検索インデックスを作成した後に、SQL そのものを変更する必要がない！**
        - `LIKE %{文字列}%` による部分一致検索のためのインデックスになっている
- Cloudflare
  - Hono
    - あらゆる JavaScript ランタイム上で動作する
    - 特定のランタイムに依存した機能を使わない
    - バカ軽量
      - Cloudflare Workers をはじめとする CDN エッジ上のランタイムでの利用ではかなり助かる
    - Cloudflare Workers との自然な連携！
      - R2/KV
  - js ランタイム
    - Node.js
    - Bun, Deno,
    - Cloudflare Workers
      - あ、これってランタイムの一種なんか
- shell
  - `ps a` の STAT
    - `+` がついてるのがフォアグラウンド
  - シグナル
    - SIGTTIN
      - バックグランドプロセスの端末入力
    - SIGTTOU
      - バックグランドプロセスの端末出力
  - tcsetpgrp

## ドメイン駆動開発

### 概要

- 考え方
  - 複雑な業務ロジックに焦点を合わせる
  - モデルに基づいた設計
  - 頻繁なリファクタリング
- 複雑なロジック
  - 競合優位性を出すには、複雑な業務ロジックが必ず必要！
- モデル
  - **分析モデル**
    - 業務内容や要求を理解するためのモデル
  - **設計モデル**
    - ソフトウェアを実際に作るためのモデル
- ドメイン駆動設計では、この2つを一致させることに価値を置く
- 境界づけられたコンテキスト
  - **1つの言葉が1つの意味を持つべき**
    - そうならないのであれば、コンテキストを分け、複数のユビキタス言語を作る
- リポジトリ層の設計スタイル、以下の2つの選択肢がある！
  - 集約の最新状態の永続化と再構築
  - **コマンド（記録）とクエリ（参照）の分離**

### ユビキタス言語

- ユビキタス言語を導入するだけでも、十分な効果が得られるんど絵はないか
- プロジェクトにおいて、**そのチームが解決しようとしてる課題に対する、現時点での解像度を示したもの**となっている
- **日本語と英語を決める**
- 決定したユビキタス言語の使用を促す！
- Command Query Separation: CQS

## Tsurugi

- 想定環境
  - コアがいっぱいある
  - 大容量メモリ
  - cf:
    - 従来の RDB のアーキテクチャ
    - コア少なめ・メモリ貴重・ベースはディスク
- Serializability の一貫性を保証？
- 用途に応じた API を用意している
- **Hybrid Concurrency Control**
  - 商用サポートレベルで提供できてる RDB は Tsurugi だけ！
  - バッチ処理のパフォーマンスが高い！

``` sh
# docker pull ghcr.io/project-tsurugi/tsurugidb:latest
```

## LLM

- LangChain のバージョン
- 0.1 以降のバージョニングルール
  - 公開 API に変更が加わるとマイナーバージョンアップ
  - バグフィックスや新機能追加、パッチバージョンアップ

## Links

- [メッセージ連携からイベント駆動型へ (AWS)](https://aws.amazon.com/jp/serverless/patterns/eda/)
- [イベントアーキテクチャとイベントストリーミング](https://www.infoq.com/jp/news/2017/10/events-streaming-kafka/)
- [AWS CDKとTerraformどちらを使うのが良いのか？ (qiita)](https://qiita.com/luton-mr/items/afe70781807bf3b5016a)
  - cfn: CloudFormation
- [Cloudflare Workersプロキシパターン (Zenn)](https://zenn.dev/yusukebe/articles/647aa9ba8c1550)
