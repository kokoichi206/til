## なんでも

- Deno2
  - Nodejs の作者が Deno を最初に作った
- SSL 証明書
  - **ドメイン所有権確認**
    - Domain Control Validation
    - Baseline Requirements (not RFC)
      - **CA/Browser Forum**
    - どれか
      - DNS 認証
        - TXT レコード, CNAME
      - HTTP 認証
        - ファイルを置く
        - `example.com/.well-known/pki-validation`
      - メール認証
  - DNS 認証
    - `トークン.example.com`
- PHP
  - Readonly
  - Intersection types
  - Property hooks
- RAG 評価ツール
  - Ragas
  - ARES
- 単体テスト
  - CQS: Command Query Separation
- 開発者体験
  - **アーキテクチャがすべて**
    - **既存の製品にはない画期的なアーキテクチャがあればこそ、ビジネスを拡大できる**
- RDB と時間
  - **時間枠の検索の難しさ**
  - Postgresql の TSRANGE
  - multirange 型
    - **GiST インデックス**
  - **PostgreSQL の排他制約**
    - https://www.postgresql.jp/docs/11/ddl-constraints.html

``` sql
CREATE TABLE schedule (
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  reservation_time TSRANGE NOT NULL,
  EXCLUDE USING GIST (reservation_time WITH &&)
);

INSERT INTO schedule (name, reservation_time)
VALUES
('a', '[2024-01-01 10:00, 2024-01-01 12:00)'),
('b', '[2025-01-25 11:00, 2025-01-28 13:00)')
;

-- これは範囲に重複があるので制約でエラーになる！！
INSERT INTO schedule (name, reservation_time) VALUES
('a', '[2024-01-01 10:00, 2024-01-01 12:00)'),
('b', '[2025-01-01 11:00, 2025-01-01 13:00)')
;

SELECT * FROM schedule
WHERE reservation_time @> '2024-01-01 11:00'::TIMESTAMP
;

SELECT * FROM schedule
WHERE reservation_time && '[2024-01-01 11:50, 2024-01-01 13:00)'::TSRANGE
;
```

- RAG
  - uv:
    - https://github.com/astral-sh/uv
    - 高速な Python のプロジェクトマネージャー
    - Rust 製

## 認証技術

### 従来

- ユーザー認証
  - **一般に、本人確認（Identity Verification, Know Your Customer）の仕組みの一部**
    - 当人認証（Authentication）
    - 身元確認（Identity Proofing）
  - 当人認証
    - **ユーザーが登録済みの本人であることを確認する**プロセス
    - **識別 + 検証**
- パスワード認証
  - ユーザー認証の中の1つ
  - ユーザーへの課題
    - パスワードを忘れる
    - 同じパスワードを使い回す脆弱性
    - フィッシングサイトに入力してしまう
  - **リスクベース認証**
    - 普段と異なる環境からのアクセスを検出し、必要に応じて追加の確認手段でユーザー本人確認する
- 認証多要素
  - 認証要素
    - 知識 SYK
      - Something you know
    - 所持 SYH
      - Something you have
    - 生体 SYA
      - Something you are
  - 所持
    - OTP
    - TOTP
      - Time-based One-Time Password
    - Microsoft Authenticator
  - 生体情報
    - **一度デジタルデータとして第三者に盗まれた場合ユーザー側で変更できない**
      - **ネットワークを介さず端末内で処理される形が現状多い**
    - False Negative, False Positive の問題がある
- 課題
  - 多要素認証を利用できない状況
    - **カスタマーサポートの負荷が増える可能性**
    - **⇨ バックアップコードの提供**
      - **緊急時に認証を続行できる仕組み**
  - 中間型フィッシング攻撃
    - **ブラウザのアドレスバー自体が偽装されているケースもある！？！？**
    - フィッシング体制のある認証方式
      - WebOTP
      - Web One-Time Password

### パスキー

- FIDO 認証
  - パスワードレス認証方式の1つ
  - FIDO アライアンスと W3C の2団体によって仕様が策定されている
  - 登場人物
    - サービス
      - Relying Party
    - デバイス
      - 認証機: Authenticator
    - ブラウザ
      - Client
- key point
  - 安全性
  - 利便性
- **デジタル署名の基本的な仕組み**
  - 送信時
    - 識別子・有効期限などのメタデータ
    - **全体に対して、秘密鍵を使いデジタル署名の作成**
  - 受信時
    - デジタル署名を公開鍵で検証
- **FIDO 認証は、このデジタル署名の仕組みを、ユーザー認証に適応したもの**
  - デバイスの登録
    - 安全な領域に秘密鍵を保存する
    - **FIDO クレデンシャル**
  - サービスが認証要求と共にチャレンジ生成
    - ランダムな値
  - デバイスは秘密鍵を用いてチャレンジを含むデジタル署名の生成
  - サービスはそのデジタル署名を公開鍵で検証
- FIDO 認証が OTP より安全な点
  - **サービスごとの**鍵ペアが生成される
- FIDO
  - 所持 + 知識 or 生体
  - 中間型フィッシング攻撃を防げる
    - WebAuthn API
- **パスキー**
  - FIDO 認証の仕様を拡張
  - **FIDO 認証のリカバリー問題の解消**
  - **モバイル端末を中心にしたクロスデバイス環境の具体的なユースケース**
  - c.f. FIDO 認証
    - パスキー
      - FIDO 認証の FIDO クレデンシャル
    - パスキーはパスワードマネージャーに保存
      - FIDO はデバイスの安全な領域保存
  - 特定機能のみパスキーを強制するなども作戦としてはあり
    - モバイル端末中心のサービスではパスキーの必須かが効率的かもしれないし、
    - クロスデバイス環境を前提としたサービスでは柔軟な導入が必要

### パスキーの仕組み・実装

- FIDO2
  - WebAuthn
    - W3C によって策定された Web の認証仕様
    - JavaScript の API を通してクライアント側で認証
  - CTAP
    - Client to Authenticator Protocol
- しくみ
  - 公開鍵、秘密鍵を利用した、チャレンジレスポンスのしくみ
  - 認証機が RP(Relying Party) サーバの識別子を含むチャレンジで署名する
    - ⇨ 偽サイトに誘導するタイプのフィッシング攻撃に耐性がある！
- **Passkeys Playground**
  - https://learnpasskeys.io/ja

## Web API テスト

- Web API テストのカバーする範囲
- E2E テストの範囲
  - サービス間からインフラ・ランタイムまでより広範囲を巻き込んでテスト
  - 最終的なエンドユーザーの体験に対する信頼性を得られる

### check 項目

- API はインターフェース
  - Web API はその Web 版！
- 確認すること
  - インタフェースの品質
  - 信頼性
  - セキュリティ
- 確認しないこと
  - モジュールレベルの信頼性
    - ユニットテスト
  - ユーザー操作・UI レベルの振る舞い、
  - ビジネス要件
    - E2E テスト
- コントラクト
  - これは OpenAPI とかで担保
- CRUD 操作とデータの一貫性
  - 冪等性が期待されない操作が重複して行われた場合、リソースが重複しない、ユニーク性が保たれるかどうかなど
- API バージョンの互換性
- エラーハンドリング
- **セキュリティ面のチェック項目**
  - 認証・認可設定
    - オブジェクトレベルの認可
  - 無制限のリソース消費
    - **API Gateway で一元的にレート制限を構成する**
  - データの漏洩・過剰なデータ露出防止
  - 入力データのバリデーション
  - HTTP ヘッダのセキュリティ設定
- **パフォーマンスのチェック項目**
  - 高負荷時
  - 長期安定
  - スケーラビリティ
- **計測すべきメトリクス**
  - レイテンシー
    - p95, p99 が許容範囲内か
  - スループット
    - API が１秒間に処理可能なリクエスト数
  - エラーレート
    - 5xx 系および 4xx 系のエラーレスポンス率
  - システムリソース使用状況
- **心掛けること**
  - シフトレフト
  - 優先順位でのテスト自動化
  - API ドキュメントの整備
- テストカバレッジちゃんと出そうね

