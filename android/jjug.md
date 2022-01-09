## Kotlin を研究する
- サーバーサイド Kotlin の人
- Ktor (ケイター)

### Kotlin とは何か
- オブジェクト指向・関数型どちらでもかける
- Java と相互運用可
- 設計の議論とかも OSS で管理されている！？

#### Java と比較した優位性
- コード量をやく 40 パーセント削減
- 型サポートの充実
- リッチな表現力

#### サーバーサイド
- サイバーエージェント、LINE,Yahoo, ビズリーチ, DMM, SanSan, PayPay
- NewsPicks: 2021/09

### Kotlin の思想
> If I were to choose one word to describe Kotlin's design, it would be pragmatism

#### Pragmatic
DX(開発者体験)を非常に重視している

- Kotlin が新しく発明した機能・概念はごくわずか
- elegance なことは大事だが、useful なことが１番の目標
- カンケチで安全なコードが書ける
- 既存のコードやツールとの互換性を非常に重要視している
- 言語だけでなく開発環境も同時に重要

### 実際の仕様

#### Immutable 変数
基本的には immutable を使う

mutable だとメンテナンス性が低い

#### Data Class
単なるデータの箱としてクラスを利用したい時には data class を使う

便利なメソッドが用意されている

#### デフォルトではクラス継承不可
継承より委譲

open をつける必要がある

継承は変更容易性が低くなり多用すべきものではない

#### 関数定義の柔軟性
関数はトップレベルへの定義やネストが可能

#### 拡張関数！！
任意のクラス・オブジェクトに対し好きな関数を生やすことができる機能！

#### Null Safety
nullable なかた宣言で NPE を回避できる

```kotlin
println(empty ?: 0L)  // 0
println(empty?.plus(456L))  // null
```

### 標準ライブラリ
Kotlin 標準ライブラリとして洗練された API で関数を提供しつつ、Java 標準ライブラリと同じ名前にしたり内部的に利用するケースが多い

#### Collection
Java 同様、List, Set, Map がある（デフォで Immutable）

Collection に関わる関数が色々用意されている

#### 例外ではなく　null を返す API デザイン！
OrNull と言う postfix がつくメソッドが非常に多い

- toInt()
  - toIntOrNull()

例外ではなく null や専用型を返すものを使う！

そっちの方が Kotlin っぽい

- Java には検査例外という仕組みがあったが、例外チェックのためのボイラープレートコードが増えるため、Kotlin では使えないようにした
- 例外自体は Kotlin で使えるが、例外は予期せぬ問題発生時のみに投げるようにし、なるべく途中ではキャッチせずトップレベルでキャッチするようにする
- 想定している異常系処理は null や専用型で対処する


### 実装パターンから見る

#### ビルダーパターン
名前付き引数・デフォルト引数で実現可能（ビルダークラスは不要）

#### 遅延評価変数
標準ライブラリでサポートされている（委譲プロパティという機能を利用）

```kotlin
class BigTable {
    val rows by lazy {
        println("heavy operation")
        listOf(1, 2, 3)
    }
}
```

#### DSL（ドメイン固有言語）
高階関数を活用することで作ることができる

```kotlin
// DSL コード
httpPost {
    host = "localhost:8080"
    path = "/path"
}
```

#### クラス委譲
簡潔なコードで　Delegation パターンを実装可能（"継承より委譲"の原理）


### 今後の　Kotlin

#### ロードマップ
- Kotlin コンパイラのかき直し
  - frontend でのコンパイラのかき直しは、ユーザー体験に直結する
- Kotlin IDE のパフォーマンス安定性の向上
- JVM サーバサイドでのユースケースについてのサポート拡充
- Multiplatform Mobile へのサポート強化
  - 現在は Alpha バージョンで、2022/4 に Beta バージョンリリース予定
  - いろんなコードをシェアできるのが理想だよね

### 質問
- エラー系の処理は、大外に投げる、ハンドリングしないのが普通
  - フレームワークに向かって投げていく
- 


## イベント駆動開発

なんか諦めた

