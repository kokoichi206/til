## chap1

- プログラミングに必要なのは、創造的な心と思考を整理する能力だけ
- 頭に描きさえできれば、コードには起こせる
  - 一番の限界は、システムに対する我々の認知能力
  - ⇨ そこに負荷をかけないよう、"複雑度"を下げることが重要
- 複雑度の下げ方
  - コードをシンプルで明確にし、複雑度を下げる
  - 複雑度を閉じ込める
- ソフトウェア設計
  - 本質的に、物理的なシステムより複雑である
  - 初めから十分にビジュアライズできない
    - 初めに建てた設計は、多くの問題があるのが普通！
  - ⇨ ウォーターフォールはうまくいかない
- 漸進的なアプローチ
  - アジャイル開発
  - 漸進的 ↔︎ ソフトウェア設計は**決して**終わらない
- 設計スキルを向上させるには
  - red flags に気づく方法を学ぶ
  - 必要以上に複雑になっているである箇所のこと

## chap2

- "複雑度"
  - 理解が難しい
  - システムの変更を行いにくい
- 複雑度が高いと...
  - 変更箇所の増大
    - 一つの修正に変更が必要なファイルが多い
  - 認知的負荷
    - 仕様を理解するのに時間・労力がかかる
  - unknown unknowns
    - 影響がある箇所にそもそも気づけない
    - バグが出て初めて気が付く。。。
- 複雑度に影響する要因
  - 依存
  - あいまいさ
- 複雑度はどんどん蓄積していく

## chap3

- ソフトウェア設計に最も大切な要素は、**マインドセット**
  - ×: tactical approach
    - 戦術的アプローチ
  - ○: strategic approach
    - 戦略的アプローチ
- tactical approach の悪い点
  - 一度入ると抜けられない
  - 複雑度がどんどん蓄積してしまう
  - スタートアップであっても、やるべきではない
- strategic approach
  - 問題を見つけたら、時間を少し使って改善すべき
  - up-front investiment は 10-20% ほどのコストを使うのが良い！

## chap4

- Modular design
  - モジュールはクラス、サブシステム、サービスなど様々な形をとる
  - どうしたって関数を呼び出す必要があり、依存性をゼロにはできない！！
- 依存性を小さくする方法
  - インターフェースと実装
  - インターフェースは、モジュールの利用者が知るべき情報全て
    - システムの他から複雑な実装を隠蔽できる
- モジュールは、インテーフェースと実装からなるユニット
- 抽象化
  - 重要でない詳細を省き、実態を簡潔にすること
  - 二つの方向で失敗しうる
    - 不要な情報が残ったまま
    - 必要な情報を抜いてしまってる
- 良いモジュール
  - パワフルな機能を提供
  - シンプルなインターフェース
  - Deep module を目指そう
- 良い例
  - UNIX I/O
  - garbage collection
- 悪い例
  - small class
  - Java class library
  - 選択肢があることは良い、ただインターフェースはできるだけよくあるユースケース例に沿って設計すべき！
