## sec 1

- User Agent
  - Web においてユーザーが安全にブラウジングするためには使用するクライアント
    - Web ブラウザが代表的なもの
- Client <-> Server での仕様
  - URL
  - HTTP
  - HTML
- **universality**
- クライアントサイド Web システム
  - Javascript エンジン
  - Web ブラウザが Javascript 向けに提供してる XHR や Fetch API
- Web ブラウザベンダ
  - リソース間の隔離
    - 論理的な隔離
    - プロセスレベルの隔離
- Web ブラウザのデータストレージ
  - Web Storage
    - JavaScript からしかアクセスされない
      - ⇨ 論理的な隔離とプロセス分離で事足りる
  - Cookie
    - JavaScript に**加えて HTTP リクエストを通して外部に送信される**
      - ⇨ **論理的な隔離とプロセス分離では不十分**
      - **セキュリティに関心を寄せる必要がある**
- 注意すべきところ
  - リソース間の論理的な隔離
  - リソース間のプロセスレベルでの分離
  - COokie のセキュアな取り扱い
  - 出入りするリソースの信頼性

## sec 2

- オリジン、というセキュリティ境界
- SOP: Same Origin Policy
- Web リソース
  - URL
    - Uniform **Resource** Locator
- Web リソースから Web リソースへの操作
  - ブラウザ内アクセス
    - Fetch API で取得したリソースに対する操作
  - ネットワーク越しアクセス
    - a, form, Fetch API
  - 埋め込み
    - iframe, img
    - script, link
- 単純リクエスト
  - a, form などで自然に発生するような HTTP リクエストのこと
- Origin
  - スキーム
  - ホスト
  - ポート
- オリジンをセキュリティの境界とする
- SOP: Same Origin Policy
  - Cross-Origin に対する
    - **ブラウザ内アクセス** を禁止
    - **ネットワーク越しのアクセス** を**部分的に**禁止
  - SOP のもとで動作する Web ブラウザ

## sec 3

Web ブラウザのレンダラプロセスの概要

- 既存の Web リソースとの互換性を保ったままプロセス分離
- 登場人物
  - Browsing Instance
    - ウィンドウやフレームの集合
    - 『つながり』を持つ
  - Site
    - スキーム + eTLD+1
    - Registrable Domain
      - URL Standard
      - https://url.spec.whatwg.org/#host-miscellaneous
      - おおよそ PSL + 1
      - PSL = effective TLD
  - Site Instance
    - Browsing Instance の部分集合
    - **同じ Site を持つウィンドウ同士からなる集合**
- CPU の投機的実行
  - Transient Instruction
    - 投機的実行がなされたが実際に ISA (Instruction Set Architecture) レベルの状態に変更を加えない命令
  - サイドチャネル攻撃
    - Microarchitectual Attack
- memory disclosure attack
  - メモリ内容が読める => （ログイン済み等の）サイト内情報が読めてしまう
  - Process-per-Browsing-Instance モデルのブラウザは、この攻撃に対して脆弱
  - => Process-per-Site-Instance モデルでの実装にする
    - レンダラプロセスの分割
- CORB: Cross-Origin Read Blocking
  - **レンダラプロセスに渡る前にブロックする！**
  - 対象リソース
    - JSON/HTML/XML
- CORP: Cross-Origin Resource Policy
  - 開発者側がオプトイン式で組み込める
- Site Isolation の実装
  - 実装コストが高い
  - パフォーマンスが多少低下する
- **Fetch Metadata**
  - https://developer.mozilla.org/ja/docs/Glossary/Fetch_metadata_request_header  
  - ブラウザがリクエストに含めるヘッダ
  - e.g.
    - Sec-Fetch-Dest ヘッダ
    - Sec-Fetch-Mode ヘッダ
    - Sec-Fetch-Site ヘッダ
    - Sec-Fetch-User ヘッダ

