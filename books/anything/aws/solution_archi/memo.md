## ASS
過去問を5,6回やる。脊髄反射。パターンプラクティス

100~1000点、720点以上で合格。10問は間違えてOK

AWSが押したいサービスが正解になる方が大きいよね。。。

### AWS Cloud Tech
１周目から、同じ問題を2回やる（1-10->1-10）

#### 2/24:19:31~
1回目の ok は確認したこと

- 1-10:
    - ok
    - 3, 
    - 3, 4, 5
- 11-20:
    - ok
    - 20,
- 21-30:
    - ok
    - 26,
- 31-40:
    - ok
    - 34,
- 41-50:
    - ok
    - 42, 46, 48, 49
    - ,
- 41-50:
    - ok
    - ,
- 51-60:
    - ok
    - 55,
- 61-70:
    - ok
    - ,
- 71-80:
    - ok
    - 78,
- 81-90:
    - ok
    - 83, 84, 88, 
    - ,
- 91-100:
    - ok
    - 97,
- 101-110:
    - ok
    - 103,
- 111-120:
    - ok
    - 114, 119,
- 121-130:
    - ok
    - ,
- 131-140:
    - ok
    - 137,
- 141-150:
    - ok
    - 144,
- 151-160:
    - ok
    - ,
- 161-170:
    - ok
    - 167,
- 171-180:
    - ok
    - 178,
- 181-190:
    - ok
    - 181, 187
- 191-200:
    - ok
    - ,



#### memo
- Amazon Lex は、音声やテキストを使用して対話できる機能をアプリケーションに簡単に追加できるサービスです。Amazon Lex では、音声のテキスト変換には自動音声認識 (ASR)、テキストの意図認識には自然言語理解 (NLU) という高度な深層学習機能が使用できます。
- NATゲートウェイは、VPC内に構成した「プライベートサブネット」からインターネットに接続するためのゲートウェイ
- ELBにはALB, NLB, CLBの三種類があり、それぞれ異なる特徴を持っています。用途に応じた最適な選択を心がけましょう。
    - ALB
        - ホスト名、HTTPヘッダ、リクエストメソッド、送信元IPアドレス等でルーティング可能
        - OSIモデルの第７層であるアプリケーションレイヤーで機能
    - NLB
        - OSIモデルの第４層であるトランスポートレイヤーで機能
        - 静的なIPを持てる
        - 急激なアクセス増加（スパイク）に対応できる
- シャーディングはDB内の複数のテーブルにデータを分割するための一般的な概念
- 可用性の高いシステムを構築するためには、Design for Failureという考え方
- MFAとは多要素認証のこと
- S3には静的ファイルをWebホスティングする機能があります。
    - https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/userguide/WebsiteHosting.html
    - 単独では、独自ドメインでSSLを使ってホスティングすることができず、動的ファイル（PHPやRuby, Python, Goなどを使ってサーバーサイドで動くプログラム）は動かないなどの制限がありますが、CloudFrontとACM、S3を組み合わせて大変よく使う構成です。
- Route53
    - DNSサービス
    - DNSサーバがポート（ルーティング）53番を使うことから由来している
- Amazon SQS(Simple Queue Service)
    - メッセージキューイングサービス
- Amazon ALBはELBの1つで、レイヤー7で動作し、パスベースルーティングやヘルスチェックなどの機能を有しています。
- 50TB などの大容量データの転送には、AWS Snowballが適しています。
    - 10TB 未満の場合、Snowboall は費用対効果の観点で最適な選択ではないケースがあります
- 安全なネットワーク接続や一貫したスループットが必要な場合、VPN よりも Direct Connect が適しています
    - VPN はインターネット経由ですが、Direct Connect は専用線が提供されるため、費用面の優先度が高くない場合は、Direct Connect が適していると言えます
- プライベートサブネット上に S3 バケットは作成できません。また、同じリージョンに S3 バケットを作成しても、インターネット経由でのアクセスが必要となります。
- リードレプリカとは更新用データベース（マスター）からレプリケーションされた参照専用のデータベースです。
- スケーリングクールダウンは、Auto Scalingが連続で実行されないようにするための待ち時間
    - Auto Scalingを設定していても、即時で問題は解決されず数分程度かけて改善されていく
- Amazon Aurora
    - MySQL および PostgreSQL と互換性のある、クラウド向けのリレーショナルデータベースです。
    - 標準的な MySQL データベースと比べて最大で 5 倍、標準的な PostgreSQL データベースと比べて最大で 3 倍高速
- S3
    - S3では、同時にマウントおよびアクセスできない
    - Amazon S3 Intelligent-Tiering
    - 「強い一貫性」が保証されている
- ElastiCache
    - 高スループットかつ低レイテンシーなインメモリデータストアからデータを取得して、大量のデータを扱うアプリケーションを構築したり、既存のアプリケーションのパフォーマンスを改善したりすることが可能
    - 完全マネージド型の インメモリDB
- ECS
    - ECSのコンテナレジストリをECR以外とするのはトリッキーな構成となるため推奨されていない
    - Amazon Elastic Container Registry (ECR) は、完全マネージド型のコンテナレジストリ
- DR（Disaster Recovery：ディザスタリカバリ）
- フェイルオーバー
    - Route53のヘルスチェック機能を使うことで、EC2の状態をチェックして異常が検知された場合には対象のインスタンスにアクセスを振り分けないようにすることができます
- Cloud Front は、静的及び動的な Web コンテンツの配信を高速化するサービス
- セキュリティグループはステートフルです。ネットワークACLはステートレスです。
    - ステートフル：ルールで許可された通信の戻りの通信も自動的に許可される
    - ステートレス：通信の行き（アウトバウンド）と戻り（インバウンド）で、ルールの設定が必要
    - ACL: 上から順にルールが適用される
- 一つのリージョンに作成できるサブネットの上限数は200
- Fargate
    - AWS Fargate により、Amazon EC2 インスタンスタイプの選択、クラスターのプロビジョニングとスケール、各サーバーのパッチ適用と更新を実施する必要がなくなります
- AWS Glue
    - データの加工などを行う、ETL（抽出・変換・格納）サービスであり、主にデータを分析する前に使うサービス
- AWS Quicksight
    - ML Insights を含むインタラクティブなダッシュボードを簡単に作成して公開できるBIツールです
- Amazon RedShiftは大量のデータ分析に使用するサービスですが、S3のデータを分析することはできません
- IOPS【Input/Output Per Second / I/O毎秒
- AWSでサーバレスアプリケーションといえば、Amazon Lambdaになります。
- S3にセキュリティグループは設定できません
- Redshift
    - レポーティングやBIに活用
    - DWH: Data Ware House
- DynamoDB
    - 高性能なNoSQL型のKVS
- Elastic Beanstalk
    - Java、.NET、PHP、Node.js、Python、Ruby、Go および Docker を使用して開発されたウェブアプリケーションやサービスを、Apache、Nginx、Passenger、IIS など使い慣れたサーバーでデプロイおよびスケーリングするためのサービス
- [EC2のインスタンスタイプ](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/instance-types.html)
    - I3は、ストレージ最適化インスタンス
        - 数万回の低レイテンシーとランダムI/Oオペレーション/秒（IOPS）をアプリケーションに提供するよう最適化
    - T2は汎用インスタンス
    - R5はメモリ最適化インスタンス
    - A1は旧世代のインスタンスタイプ
- サブネットのトラフィックがインターネットゲートウェイにルーティングされる場合、そのサブネットはパブリックサブネットと呼ばれます。
- IPS (Intrusion Prevention System)は、不正侵入防止システムである。ネットワークやサーバーを監視し、不正なアクセスを検知して管理者に通知する役割を担うシステムとしてIDS（Intrusion Detection System：不正侵入検知システム）があります。
    - インスタンスまたはリバースプロキシ層に IDS/IPS エージェントを実装することで解決できます。
- IAMを利用して最適なセキュリティ上のベストプラクティスに沿うためにはアクセスレベルを使用して、IAM 権限を確認することが必要
    - 5 つのアクセスレベル (List、Read、Write、Permissions management、または Tagging)
- AWS Transit Gateway を使用すれば、中央のゲートウェイからネットワーク上にある Amazon VPC、オンプレミスのデータセンター、リモートオフィスそれぞれに単一の接続を構築して管理することができます
- メッセージキューは、サーバーレスおよびマイクロサービスアーキテクチャで使われる非同期サービス対サービスの通信形態で
- EC2インスタンスを複数AZにスケーリングする場合は複数AZに跨いだトラフィック分散を可能にするELBにAuto Scalingを設定することが必要
- AWS DataSync は、オンプレミスストレージと Amazon EFS 間でデータを迅速かつ簡単に移動することができるマネージド型のデータ転送サービスです。
- ELBはリージョンサービスであるため、複数のAZまでしか振り分けることができません。
    - Application Load Balancer
    - Network Load Balancer
    - Gateway Load Balancer
    - Classic Load Balancer
- EBSは「EC2とセットで使うストレージ」
- DynamoDB
    - データ容量が1アイテム当たり400KBと制限があり
    - https://aws.amazon.com/jp/dynamodb/
- Amazon マシンイメージ (AMI) 
- 複数バージョンのオブジェクト維持を可能なバケットのHTTPリクエストで503レスポンス
    - バージョニングを有効にしたバケットへの Amazon S3 PUT または DELETE オブジェクトリクエストが実行された場合に当該エラーが発生してしまう原因としては、数百万のバージョンが存在している1 つ以上のオブジェクトが存在している可能性があります。数百万のバージョンを持つオブジェクトがある場合、Amazon S3 は、過剰なリクエストトラフィックからユーザーを保護するためバケットへのリクエストを自動的に調整します。
    - この問題を回避するためには、ライフサイクル管理の「NonCurrentVersion」有効期限ポリシーと「ExpiredObjectDeleteMarker」ポリシーを有効にして、以前のバージョンのオブジェクトを期限切れにし、バケット内に関連するデータオブジェクトが存在しないマーカーを削除します。したがって、「オブジェクトのライフサイクル管理を設定する。」
- EMR: Elastic MapReduce
    - S3やDynamoDBなどのAWSサービスと連携
    - ビッグデータの処理及び分析
- OAI: Origin Access Identity
    - S3に配置したファイルへのアクセスを制限

#### LambdaとAPI Gatewayを連携させ
APIコードを変換して、Lambda関数とAPI Gatewayを使用したサーバレスアプリケーションに移行することが可能です。Lambdaでは関数の実行時間にのみ料金を支払うためコストを節約できます。また、API Gatewayを利用することでAWS Lambda 関数をHTTPSリクエスト経由で呼び出すことができます。

ELBをパブリックサブネットに配置しその後ろにEC2を配置することで、EC2インスタンス上に構成したWebサービスをインターネット上に公開しています

CloudWatch Logs は、アプリケーション、AWS サービスからのログを一元管理できる、スケーラビリティに優れたサービス


### 問題集
- メッセージングアーキテクチャの一般的な使い方
    - RDSのイベント通知からSNSのトピックを送信し、さらに並行非同期処理のためにSQSのキューに格納する
- AWS WAF の Web ACL 機能により、国単位のアクセス制限を行える
    - セキュリティグループとネットワークACLには、国単位のアクセス制限機能はない
    - Access Control list
    - AWS WAF に対応しているサービス
        - API Gateway
        - CloudFront
        - ALB
        - AppSync GraphQL API
- Network address translation (NAT) gateway
- サイト間VPN：Site to Site VPN
    - AWSとオンプレミス感をVPNでセキュアに接続できるサービス
    - インターネット経由のため、高速かつ安定した通信は期待できないが
    - すぐに構築でき、構築費や運用費も安価である
- Storage Gateway を利用すると、オンプレミスで作成されたデータのバックアップをAWS上に自動で取得することができる。
    - Storage Gateway には、ファイルゲートウェイ、ボリュームゲートウェイ、テープゲートウェイという３つのゲートウェイタイプがある
- Global Accelerator
    - 複数のリージョンに跨ったALBやNLBに対してトラフィックを振り分けることが可能なマネージドサービス
    - 静的なIPアドレスを提供するため、ファイアウォールの許可設定を行いたい場合に有効
- OAI
    - S3バケットへのアクセスをCloudFront経由のみに制限するには、オリジンアクセスアイデンティティ（OAI）機能を利用する
- NLB
    - 通信の遅延を抑えながら秒単位で大量のリクエストを処理でき、かつスパイク処理にも対応できるよう最適化されたソリューション
    - リージョン間の負荷分散を最適にするソリューションではない

#### 疑問
- GateWay Load Balancer: GWLB
    - ELBの一つ
    - セキュリティ製品などに負荷分散する？



### 黒本
- IAMユーザー作成直後、権限は付与されて**いない**
- AWS CLI や SDK を利用するには、IAMユーザーのアクセスキーIDとシークレットアクセスキーが必要
- NAT ゲートウェイは複数のAZに冗長化できない
- ELBとSQSはAWS内部で冗長化されているため、SPOFになることはない
    - IGW: Internet GateWay も
- プライベートサブネット内のリソースからインターネトへ接続するためには、NATゲートウェイを配置する
    - NATゲートウェイは、AZ内では冗長化
    - AZ間の冗長化はされていない
- GoogleやFacebookなど、OpenID ConnectをサポートしているソーシャルネットワーキングサービスをIDフェデレーションで連携させることで、AWSへのシングルサインオンが可能。これを「Web IDフェデレーション」と呼ぶ
- Webアプリケーションやモバイルアプリからの認証では、Amazon Cognitoが便利

#### 疑問
- Elastic ip
    - 固定のグローバルIPアドレスを提供するサービス
- Elastic Beanstalk
- CodeDeploy
- OpsWorks


## memo
- 三層アーキテクチャのドメインの設定など
    - Web 3層構成
- インスタンス購入オプション
    - https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/instance-purchasing-options.html
- [AWS Well-Architected フレームワーク](https://docs.aws.amazon.com/ja_jp/wellarchitected/latest/framework/wellarchitected-framework.pdf)
- AWSのRoute53でDNSのレコードを設定すると、世界中のDNSサーバにコピーされるから、ものすごく信頼性が高い。自社サイトのDNSサーバとして使うもアリですよ

## やってみたいこと

### Amazon API Gateway
API の公開から保守運用までを一貫的に行うことができる。さらに、AWS WTF により後悔した API を脅威から保護できる。

IAMデータベース認証では、IAMロール認証情報と認証トークンを使用してRDSのデータベースインスタンスに接続できる。データベースのユーザー認証情報を保存する必要がないため、ネイティブ認証方法よりも安全に接続することが可能。

API Gateway 配下で稼働させるコンピューティングサービスについて、Lambdaとコンテナのどちらが適するか。コンテナについては、オーケストレーションサービスとしてECSとEKSが提供されており、その稼働環境（EC2あるいはFargate）によって特徴が変わる。

### モバイルに DynamoDB へのアクセス権限付与
アプリケーションから Google, Amazon, Facebook などのIDプロバイダーを使用してサインインし、一時的な認証トークンを取得する。認証トークンを、DynamoDB へのアクセス権限を持つ IAM ロールとマッピングする。(p198)

ベストプラクティスでは、モバイルアプリケーションにAWSリソースへのアクセス権限を与える方法として、Web ID フェデレーションを用いて取得した一時的な認証トークンを使用することが推奨されている。

### Lambda
Lambda + Security Token Service (STS)

### データ処理におけるクラウドネイティブなアーキテクチャ
SQSとLambdaを組み合わせてデータ加工を行う構成

1. S3にデータをアップロードする
2. S3のオブジェクト作成イベントがSNSに通知される
3. SNSからSQSにイベントが連携される
4. SQSのメッセージをトリガーにLambdaがデータ処理を実行する
5. Labmdaの処理が終了したらS3へデータを格納する

LambdaのトリガーとしてならばSQS Lambdaでも実装可能ですが、複数のサブスクライバー(送信先)にメッセージを受信させたい場合は、SNSが必要

### EC2からS3へのセキュリティ
- VPCエンドポイントポリシーを作成し、特定のS3バケットへの通信のみを許可する
- S3バケットポリシーを利用し、アクセスもとがVPCエンドポイントの場合のみ操作を許可する


## IOPSとスループット

### IOPS
Input Output per second。ストレージが1秒あたりに処理できるI/O（書き込み・読み込み）アクセスの数。基本的にHDDは1分あたりの回転数(RPM)の限界があるためIOPSが低い。SSDはIOPSが高い。『１秒間のストレージ書きこみ読みこみ性能』。SSDの場合、I/Oの回数寿命が比較的に短い（らしい）事に注意。

### スループット
一定時間にどれだけのデータを転送できるか？単位時間あたりでどれくらいの仕事の処理能力があるか。一定時間でどれだけデータを転送できたか。1秒あたりのデータ量をビット数で表す。『１秒間の最大データ転送量』

「トラフィック監視」「WAN高速化」「ロードバランサ」などの管理指標。コンピュータやネットワーク機器などの性能を評価する指標。「上り」は送信でアップロード。「下り」は受信でダウンロード。

IOPSはピンポイントでストレージの書き込み読み込み性能をあらわしますが、スループットはネットワーク通信速度的な指標でややスコープが広い様です。

### 最適化
ディスクのスループットが大きければアプリケーションのパフォーマンスが必ず上昇するというわけではない。サイズが4KB以下のファイルを数多く書き込む様な場合、スループットよりもIOPS の数値を重視した方がパフォーマンスが上がりやすい。逆に一度の書き込みがGB単位のような大きなサイズの場合、スループットを重視した方がパフォーマンスが上がりやすい。


## 疑問
- オンメモリ vs インメモリ?
- プライベートサブネット?
- アドホックSQLクエリ？
- Redshift
- VPC: Virtual Private Cloud
    - AWSアカウント専用の仮想ネットワーク
- マルチリージョン、マルチAZ
- S3オリジン（バケット）
