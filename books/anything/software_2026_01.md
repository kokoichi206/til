## LLM

### Basic

- 機械学習
  - データから経験的にパターンを学び取る
  - 機械学習の一分野である深層学習
  - 深層学習を自然言語に応用したのが LLM
- Transformer
  - Self-Attention
  - GPT3 ~ 数千億のパラメーター => `~10^11`
  - Attention is All You Need
- **Scaling Law**
  - 計算資源と精度のドレーどおふ
  - 3要因
    - モデルサイズ = パラメータ数
    - 学習データりょう
    - 計算量
- **LLM の処理範囲を外部資源へ拡張**
  - RAG
  - Agent

### 学習プロセス

- 事前学習
  - 自己教師あり学習
    - Next Token Prediction
  - フルスクラッチ、継続事前学習
- 事後学習
  - SFT: Supervised Fine Tuning
  - RLHF: Reinforcement Learning with Human Feedback
    - PPO: Proximal Policy Optimization
- RLHF
  - RM: Reward Model
    - 人間の好みに合うように報酬モデルを学習
  - 報酬モデルが必要、最適化が難しい
  - => DPO: Direct Preference Optimization
    - 報酬モデルが不要
    - 勝ちモデルと負けモデルのペアを使って直接最適化
- RLVR: Reinforcement Learning with Verifiable Rewards
  - 人間のフィードバックを使わずに、LLM 自身が生成した検証済みの応答を使って強化学習を行う手法
  - コスト削減とスケーラビリティ向上

### モデルの問題

- 公開されてるか
  - クローズドモデル
  - オープンモデル
    - Qwen3, DeepSeek-R1, OpenAI gpt-oss, Llama 3
- 総パラメータ数
  - **10 億 (Billion)**
  - gpt-oss - 120b => 1200億
  - **10B くらいまでが小型**とも呼ばれる
    - スマホや個人 PC などで動かせることがある
  - 100B を超えると大型かな〜
- モデルの主な組み方
  - **Dense モデル**
    - ほぼ全てのパラメータが常に使用される
    - 推論コストは高め
  - **MoE モデル**
    - Mixture of Experts
    - **複数の専門家と呼ばれるサブネットワークを持つ**
    - **入力に応じて一部の専門家ネットワークのみを使って推論**
    - **実際に使用されるパラメータ数『アクティブパラメータ数』が大幅に少ない**
    - gpt-oss-120b
      - 128 Experts
      - アクティブな Expert はそのうち4つのみ？
      - アクティブパラメータ数は 5B 程度
- Transformer 以外のモデル
  - Transformer:
    - **コンテキストの長さによって計算量・必要メモリが大きくなりすぎる問題**
    - => Memba
      - **計算量をコンテキスト帳に非依存にする**
      - 状態空間モデルでの逐次的な処理
- Reasoning モデル
  - Test Time Scaling
  - Reasoning モデルになるかどうかは基本的に学習過程によってきまる
    - **モデル構造は同一の構造にできる**
- 量子化
  - LLM のパラメータ
    - float16 が多いが、これを int8, int4 とかにすると単純に必要なメモリが減る
- 代表的なベンチマーク
  - HLE: Humanity's Last Exam
    - 人類の知識全般
  - SWE-Bench
  - HumanEval
    - プログラミング能力

## データ構造

- 組み込み系
  - OLTP
    - SQLite
  - OLAP
    - DuckDB
- DuckDB
  - データ構造
    - **ストレージレベルでの最適化**
    - **カラムなストレージ**
      - ベクトルをそのままデータ構造に落とし込んでいる
      - 分析・集計のワークロードの場合は、必ずしも全項目を必要としないため
    - キャッシュサイズの調整
      - 
  - アルゴリズム
    - **CPU のマルチコア並列処理と各プロセス最適化**

**Latency Numbers Every Programmer Should Know**
https://gist.github.com/jboner/2841832

- キャッシュ
  - LRU: Least Recently Used
  - LFU: Least Frequently Used
  - FIFO: First In First Out 

## なんでも

- TLS インスペクションサーバー
- Vitest
  - 2020, Evan You san
  - features
    - TypeScript 完全サポート
    - watch mode
    - 並列実行
    - **ブラウザモード**
    - **スナップショット**
    - モック
    - ベンチマーク
- WebXR Device API
  - Immersive Web により策定されている
  - Module
    - Plane Detection Module
- **ドメイン名のプレイヤー**
  - ICANN
    - 非営利法人
  - レジストリ
    - **1つの TLD に対して1つだけ存在する管理・運用元**
    - **権威サーバーの運用義務**
    - **Anycast** 技術による分散配置
    - DDoS の対象となりやすい
  - レジストラ
    - レジストリと契約し顧客へドメイン名を提供
    - お名前.com, GoDaddy など
    - **ICANN との契約が必要**
      - RAA: The Registrar Accreditation Agreement
    - 1つの TLD に対して複数存在可能
      - **=> 価格競争が起きる**
  - レセラー
    - ICANNとは直接契約しない
    - レジストラと再販契約を結ぶ
    - DNS権威運用もしない（= 技術的責任はほぼゼロ）
  - レジストリによる値上げ
    - インフラコストの高騰
    - セキュリティ対策
- LLMOps
  - 課題
    - **監視・ロギング**
    - **出力の評価**
    - **出力の改善**
  - Langfuse
    - selfhost 版があるのも魅力！
  - demo
    - Streamlit
  - 本番提供
    - 拡張と運用に耐える
    - 追跡可能性・再現性
  - 周辺のエコシステムの選択肢を考えて
    - Go => Python + LangGraph にした
    - **ワークフローの状態遷移をコードから把握しやすく Reducer の概念を活用したテストが書きやすい**
  - **エンジンをサービスとして切り出す**
    - ネットワークのオーバーヘッドが増える
      - が、ワークフロー全体の律速は外部 LLM API の応答速度であることがわかっていたので
- インターネットのルール
  - IETF: Internet Engineering Task Force
    - **Rough Consensus and Running Code**
    - 完璧な理論よりも動くことを重視
  - IEEE: Institute of Electrical and Electronics Engineers
    - アイ・トリプル・イー
    - Wi-Fi, Ethernet など
    - **仕様書としての性格が強い**
  - RFC
  - IP アドレス
    - **IANA**: Internet Assigned Numbers Authority
      - 大枠を管理
    - **RIR**: Regional Internet Registry
      - 5つの地域インターネットレジストリ
      - **APNIC**: Asia Pacific Network Information Centre
        - JPNIC: Japan National Information Center
    - **ICANN**: Internet Corporation for Assigned Names and Numbers
      - IP アドレスやネットワーク資源に関するルール全体の国際的な調整
