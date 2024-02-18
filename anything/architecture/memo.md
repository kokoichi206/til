## クリーンアーキテクチャについて思ったこと

- クリーンアーキテクチャにこだわる必要はない。
- 大事なのは依存性の方向が単一であること
  - つまり循環さんしょうがないってこと？
    - これは Go さんすごい
  - 方向も大事
- インフラ層（DB 周り）とユースケースの関係のみ注意
  - 素直に実装すると『処理の流れ・依存関係』と『期待される依存関係』が逆になる
  - インターフェースを使って依存性を逆転させる
  - ここのみはしっかりインターフェースを使う
    - いわゆるリポジトリパターンな気する？
- なんでインフラ層が一番外なんだっけ？
  - DB に何を選ぶかによって、ユースケース等（ドメイン層など）が影響を受けるべきではないので！
  - DB は大外にいるべきだな〜〜

### SOLID を守るために

インターフェースを使って DI を行うと、LID は守れる気がする（L は頑張り次第）

- S … Single Responsibility Principle: 単一責任の原則
- O … Open-Closed Principle: 開放閉鎖の原則
- L … Liskov Substitution Principle: リスコフの置換原則
  - [置換原則を守れてない例](https://www.membersedge.co.jp/blog/typescript-solid-liskov-substitution-principle/)
- I … Interface Segregation Principle: インターフェイス分離の原則
- D … Dependency Inversion Principle: 依存性逆転の原則

### [背景](https://qiita.com/juchilian/items/d732afab315e3c7e8ba3)

[Robert C. Martin さんの講演動画 (11'40 あたり)](https://www.youtube.com/watch?v=2dKZ-dWaCiU&ab_channel=ITkonekt?t=1180) で述べられている。

フォルダを開いたときに最初に伝わってくる情報  
→ 「何のフレームワークを使っているか？」ということ。これは、プロジェクトにおける現実の課題解決で重要なのか？

フレームワークはツールに過ぎないので、フレームワークの情報は重要ではなく、「何をしてくれるサービスか」「どこに大事な情報が格納されているか」がわかることの方が重要！

web も広く言えば i/o デバイスである。

ん、モチベーションこれだけ？

### メリット

- 将来の変更に強いアプリケーションを作ることが可能。
- ビジネスロジックが明確になる
- テストがやりやすくなる

### Entities

DDD での Entity に近いらしい（Value object ではない）。  
Entity を取り出す Repository, Domain Service とかまで含まれそう。

### Use Cases

Entities を束ねるもの

### Links

- [実装クリーンアーキテクチャ](https://qiita.com/nrslib/items/a5f902c4defc83bd46b8)
- [iOS Clean Architecture について](https://qiita.com/koutalou/items/07a4f9cf51a2d13e4cdc)
  - iOS 開発に限らない話をしてる
- [背景](https://qiita.com/juchilian/items/d732afab315e3c7e8ba3)
- [Robert C. Martin さんの講演動画: Clean Architecture and Design](https://www.youtube.com/watch?v=2dKZ-dWaCiU&ab_channel=ITkonekt)
- [Robert C さんの講演動画: Clean Code](https://www.youtube.com/watch?v=7EmboKQH8lM&ab_channel=UnityCoin)
- [プログラミング言語とシステムデザイン: Slide share](https://www.slideshare.net/tsutomuyano/ss-250915366)

## 2024

https://www.youtube.com/watch?v=yVPNvfpH_qU&t=10s

**Backend**

- ヘキサゴナルアーキテクチャ
  - https://nrslib.com/hexagonal-architecture/
  - Application が中心
    - ビジネスを中心に見立てて、それ以外を交換可能にする
  - **Port and Adapter**
    - **アプリケーションは入力デバイスを知らないし、データストアが何かも知らない**
  - ビジネスロジックを**点在させない**
- レイヤーどアーキテクチャ
  - 昨今では DI 併用
  - 依存の方向を制御する
  - 上のオブジェクトが下を知るのはいい
    - 下が上に依存するのはダメ
  - DIP を実現するために DI を使ったり
- クリーンアーキテクチャ
  - 図をベースとした発表か、本の話なのか
    - コンテキストを統一する
  - 今回図の話
  - クリーンアーキテクチャは思想のイメージ
  - flow of control, 完全に理解した
    - controller が input port を使う、依存の関係
    - input port の実装として usecase interactor が用意されるんだ、汎化の関係
    - interactor は output port を使うんだ
    - output port の実態は presenter, 汎化の関係か
  - **依存の方向は内向き**
    - **依存関係の方向はプログラマが絶対的に制御できる**
  - Pros
    - ヘキサゴナルで達成したいこと**以上を実現する**
      - 全レイヤーでどこでも単体テスト可能
  - Cons
    - かなり冗長

**GUI**

- MVC
  - Web のためのアーキテクチャではない
  - より低レイヤーを扱うことが多かった時のもの
- Classic MVC
  - GUI Pattern
- MVC2
  - Web 上で MVC をガッちゃんこしたもの
  - **MVC Framework**
- MVP
  - ビューをウィジェットとして扱う
  - **ビュートコントローラの分離を削除**する
  - ユーザーが view を直接やり取りする！
    - **昨今のスマホのような**
  - view, model 間
    - Supervising Controller
      - observe
    - Passive view
      - 明示的に presenter が view を呼び出す
      - 後発
      - **テストがしやすい**
- MVVM
  - view と viewmodel の間で data binding させる
  - MVP とちかい
  - Angular
  - React
    - 単一
  - Vuew
    - 双方向
- MVW
  - MV, and **Whatever**

**その他**

- サービス間
  - モノリシックアーキテクチャ
  - マイクロサービスアーキテクチャ
    - HTTP 等のネットワーク越しにやり取りする？
  - モジュラーモノリス
    - モジュール間の連携で開発者に分別を求める
    - データの境界の定義とかしんどい
- クラウドネイティブ
  - 構成要素
    - コンテナ
    - マイクロサービス
    - サービスメッシュ
    - 宣言的 API
    - イミュータブルインフラストラクチャ
  - 利点
    - **スケーラビリティ**
      - うむ
    - 運用コスト
    - コスト最適化
      - オンデマンド
- リアクティブ宣言
  - https://www.reactivemanifesto.org/ja
  - **アプリも形を変えないと、クラウドネイティブにならない**
  - **CQRS + ES**
- CQRS + ES
  - リアクティブシステムを構築くるための1つの解法
    - 作り方の話
  - Command Query Responsibility Segregation
  - Read model updater
  - Pros
    - インピーダンスミスマッチを避けられる
    - コマンドとクエリの異なる要件に応えられる
  - Cons
    - 伝統的な実装よりは複雑
    - システムの数が増える
- Pub Sub
  - リアクティブ, スケーラビリティ
