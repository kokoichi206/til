- 開発者の認知負荷を減らす
- 組織を分けるが DevOps が叫ばれたような分け方はしない
  - 逆戻りはしない
  - Team Topologies
- 各ベンダーがテンプレートなどを出してくれている
- スタートアップにおける実践例が増えるといいな
- 誰にとっての価値か
  - 開発者に価値を提供しなければ意味がない
- Platform as a Product を実践しようとするとプロダクトマネージャーが不足する！
- [Attributes of platforms](https://tag-app-delivery.cncf.io/whitepapers/platforms/#attributes-of-platforms)
  - User Experience
  - Documentation and Onboarding
  - Self-service
  - Optional and Composable
  - Secure by default
    - セキュア・法的に問題がないか
- 体系化・言語化されたことで、知見が明確になる！
- 認知負荷の計測
  - white paper に何か書いてある
    - 4 keys
    - [SPACE framework](https://queue.acm.org/detail.cfm?id=3454124)
- ドキュメント更新
- インナーソースの考え方
  - Open Source を自社の中に取り入れる

## [Backstage 勉強会: Platform Engineering Meetup Online#1](https://www.youtube.com/watch?v=koMsUFOar88&ab_channel=PlatformEngineeringMeetup)

### Backstage

- https://github.com/backstage/backstage
- インフラと開発ツールの抽象化
- ユースケース
  - Create
    - Software Template
      - 環境の準備
      - マイクロサービスなどを開発するためのベースリポジトリを作成可能
    - TechDocs
  - Manage
    - component を一元管理
    - Software Catalog
      - コンテキストの切り替えが不要になる
    - k8s plugin
  - Explore
    - Catalog
    - Search
- 開発者ポータルツールの1つ
  - **開発者にとっての窓口**
- 哲学
  - インタフェースとしての一元化
  - 開発者の自立性の支援
  - 明確な所有権の確率

### k8s, AWS

- Platform Engineering
- オンボーディング
  - ドキュメント
  - ポータル
  - テンプレート
- Backstage の機能
  - プラグインエコシステム
  - ソフトウェアカタログ
  - 検索
  - 技術ドキュメント
  - ソフトウェアテンプレート
- テンプレート
  - 新しいプロジェクトを素早く立ち上げる
  - 組織のベストプラクティスでツールを標準化
- backstage
  - 初期の k8s に近い雰囲気
    - 独自プラグイン
  - プラガブル・エディタブル
- なるほど

### plugins

- backstage は、プラグインのセットで構成される、シングルページのアプリ
- プラグイン
  - frontend-plugin
  - backend-plugin
  - web-library
  - ...
- **課題**
  - 開発に必要な情報が色々なところに散らばっている
- 例
  - k8s plugin
  - argo cd plugin
  - google cloud build plugin
  - sonarqube plugin
  - gh pull request plugin
  - OPA
    - Orchestrate Platforms and Applications on AWS
    - https://opaonaws.io/
- https://backstage.io/plugins/
- demo site
  - https://demo.backstage.io

### メモ

- Backstage was created by Spotify but is now hosted by the Cloud Native Computing Foundation (CNCF) as an Incubation level project
  - an Incubation level project

## Links

- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
  - Attributes of platforms
- [AWS Platform engineering](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-caf-platform-perspective/platform-eng.html)
- [Red Hat Developer Hub](https://www.redhat.com/ja/about/press-releases/red-hat-unveils-red-hat-developer-hub-help-fuel-developer-productivity)
