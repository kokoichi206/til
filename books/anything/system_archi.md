# システム設計の原則
現場で役立つシステム設計の原則

Principles of the Systems Architecture

## 場合分けのロジックを整理する
- 判断ロジックと分岐後のロジックを、それぞれメソッドに抽出する
- else 句をなくすことも考える
- 早期リターンする書き方を**ガード節**という
- 多態（区分ごとに異なるクラスのオブジェクトを「同じ型」として扱う仕組み）
  - クラスとクラスの関係は、お互いの「知ってること」を少なくする！
  - 区分ごとのロジックをクラス単位に分離してコードを読みやすくするオブジェクト指向らしいしくみ

## 三層アーキテクチャ
- MVC
  - Model, View, Controller
- プレゼンテーション層、アプリケーション層、データベース層
  - プレゼンテーション層：画面や外部接続インタフェース
  - アプリケーション層：業務ロジック、業務ルール
  - データベース層：データベース入出力

この２つどー使い分ける？

データを持つクラスに業務ロジックを集める。getter の身のメソッドを作らない。

- メソッドは必ずインスタンス変数を使う
  - インスタンス変数を使わないメソッドは、そのクラスのメソッドとして不適切
  - 置き場所を再検討すべき

## ドメインオブジェクト
- 関連する業務データと業務ロジックを１つにまとめたもの
- 三層＋ドメインモデルを目指していこ

### 三層＋ドメインモデル
- 業務ロジックを記述するのはドメインモデルだけ。
- 業務的な判断・加工・計算のロジックは、全て、ドメインオブジェクトに任せる。

### ドメインモデルの何が良いのか


## memo
- 説明用の変数の導入
  - 破壊的代入は、変更の副作用を起こしやすい
- メソッドの抽出
- 狭い関心ごとに特化したクラスにする
  - その用語の関心ごとに対応するクラスを**ドメインオブジェクト**と呼ぶ
- 業務アプリケーションをオブジェクト指向で設計する場合には、業務で扱うデータの種類ごとに専用の「型」（クラスやインターフェース）を用意する。
  - 値オブジェクト（Value Object）
    - 値オブジェクトの値は「不変」にする
    - 別の値が必要になったら、「別のオブジェクト」を作成する！
- 値オブジェクト生成
  - 業務の関心ごとを直接的に表現する
  - インスタンス変数はコンストラクタでオブジェクトの生成時に設定する
  - インスタンス変数を変更するメソッドを作らない
  - 別の値が必要であれば、別のインスタンスを作る
- 完全コンストラクタ：
  - オブジェクトの作成時に、オブジェクトの状態を完全に設定するやり方
  - String / BigDecimal / LocalDate など
- コレクションオブジェクト
  - リストやコレクションの操作などは、コードを複雑に見せてしまう
  - その関係を、全て１つのクラスに閉じ込める

