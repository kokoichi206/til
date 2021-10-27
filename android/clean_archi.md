# clean architecture

## link
- [『ドメイン駆動設計入門 ボトムアップでわかる!ドメイン駆動設計の基本』第１４章のサンプル集](https://github.com/nrslib/itddd/tree/master/CleanLike)
- [youtube(日本語)](https://www.youtube.com/watch?v=5oJeSrwztPg)
- [ADOP (Application Domain Others Pattern)](https://nrslib.com/adop/)

### クリーンアーキテクチャ
- [youtube(日本語)](https://www.youtube.com/watch?v=5oJeSrwztPg)
- [Sample Code](https://github.com/nrslib/play-clean-java)

JJUG CCC 2019 Spring

「API はできてないし、DB は構築どころか選定もできてないけど、納期だけは決まってるからよろしく！」

デザインに必要なもの → 試行錯誤

試行錯誤のために、フロントのプロトタイプを！

クリティカルパスを避け、先行して開発する方法はないか

→ The Clean Architecture

#### クリーンアーキテクチャについて
- ヘキサゴナルアーキテクチャとやりたいことは一緒
- ヘキサゴナルの外側の具体的な実装について、詳細に記載されているのがクリーンアーキテクチャ
- ビジネスロジックが詳細なコードに依存しないようにする
  - DIP(dependency injection principal)
- 依存の方向は内向き
- 内側の変更は外に影響する
- 内側は外側を知らない
- ドメインロジックで web とか db とかの言葉を使わない
- データクラスとインタフェースがあって、実装クラスがいっぱいある
- 全体像がわかれば、コードの量が増えても読みやすくなる
  - 知りたいことがどこに書いてあるかがわかる

#### 実装例
- まずコントローラー
  - コントローラー、は司令官ではない
  - ゲームのコントローラーと一緒で、入力の変換！
- 次、Input Data
  - DS: Data Structure
- Input Boundary: Input port
- Use Case Interactor
  - Application logic



## youtube
- [link](https://www.youtube.com/watch?v=EF33KmyprEQ&t=4119s)

### Api
- [v1/coins](https://api.coinpaprika.com/v1/coins)

### Clean Architecture
- MVVM in Android
- CA uses one more package: usecase
- UseCase?
  - Features
- dto
  - data transfer object
  - ここでは API の通りに受け取る！
  - domain/model で、使いたいデータだけを持った形に変える！
- repository
  - domain の repository は、インターフェースだけ
  - data の repository は、DB アクセス等を含んだ実装が入ったもの
- viewmodel は presentation
  - couple to composale
- What is ViewModel?
  - No buisiness logic (this is in usecase)
  - Just maintain our state !

### Error
- HttpException
  - // 4xx, 5xx とか
- IOException
  - // no internet connection とか


### わからんこと
- flow にしとくと、勝手に状態を更新してくれる？
- @Inject とか？
  - Hilt が全くわからん
  - @HiltViewModel ?
- sealed class ?
- @AndroidEntryPoint
- savedInstanceState
- CoinApplication がなんで必要？

### memo
- FlowRow は有能すぎん？
- lateinit
  - late init
  - 後から初期化する！？

### Hilt
- InstallIn
  - lifecycle がその（）の中のものと同じになる？

### LiveData

