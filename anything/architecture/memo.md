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
