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

## sec 4

- 匿名性
  - アプリケーション層 の情報だけから個人を一意にはできない
    - 一般に
    - stateless 性
- Cookie 属性
  - Expires
  - Max-Age
    - Expires と機能は同じ、こちらが優先される
    - **Expires や Max-Age を過去にすると削除が可能**
  - Domain
    - Public Suffix に対して Cookie のセットは不可
  - Path
  - Secure
  - HttpOnly
    - セッションハイジャッキング
      - XSS 脆弱性 (の一部) => HttpOnly
      - 通信経路の盗聴 => Secure
    - セッション固定攻撃
      - 任意のセッションをユーザーのブラウザで使わせる
      - **Cookie の数やサイズに上限があることを利用して１回溢れさせて HttpOnly の Cookie を消す**
      - => HttpOnly false の Cookie を同名で新たに作成し直せる
  - SameSite
- 3rd-party Cookie
  - eTLD + 1 が一致**しない**ホストに対するリクエストに付与される Cookie
  - 1st-party Cookie
    - eTLD + 1 が一致**する**ホストに対するリクエストに付与される Cookie
  - DNT: Do Not Track
    - DNT ヘッダ
  - **simple な禁止は『不透明なやり方』を助長することにもつながる**
    - 不透明なやり方
      - ブラウザフィンガープリント
      - **SuperCookie**
    - Chrome
      - https://privacysandbox.google.com/blog/privacy-sandbox-next-steps?hl=ja
- CSRF 攻撃
  - 原因
    - **正規の遷移を経たことを保証してくれる情報がリクエスト中にないこと**
  - CSRF トークンによる対策
- Cookie と Origin のセキュリティ境界の違い
  - Cookie のセキュリティ境界
    - ホスト名
    - パス
    - スキーム
  - Origin のセキュリティ境界
    - スキーム
    - ホスト名
    - ポート
  - e.g.
    - **ポートを分けてプロセスを立ち上げてても、片方のサイトが脆弱であれば両方の Cookie がもれる！**

## sec 5

- HTTPS
  - Secure
  - **改ざんのに対する耐性**
- HSTS
  - HTTP Strict Transport Security
  - **TOFU: Trust On First Use** のセキュリティモデル
- SRI: Subresource Integrity
  - **最初に読み出す Web ページの完全性を認めた上で、そこから読み出されるリソースの完全性を検証する**
  - https://developer.mozilla.org/ja/docs/Web/Security/Defenses/Subresource_Integrity
- Secure Content
  - Service Worker API
  - Storage API
  - Payment Request API

## sec 6

- Content Injection 脆弱性
  - e.g.
    - XSS
    - HTML Injection
  - CSP
  - 方法の1つ
    - 任意の JavaScript の実行を達成する、ことを目的にしてる
  - Scriptless Attack
    - CSS Injection でコンテンツのリーク
- サイドチャネル攻撃
  - XS-Leak
    - COSI: Cross-Origin State Inference の1つ
    - 相対性
      - TTFB 等
    - 絶対性を持つ
      - length 等

