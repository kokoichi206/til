## メモ
- 現在のDLは「多くのデータ」および「計算リソース」を必要とする
- データの種類が問題のバリエーションをどの程度カバーしているか
- 汎化能力を獲得することが大事
- オッカムの剃刀
    - ある事象を説明するのに、必要以上に多くを仮定するべきでない
- 教師あり学習と教科学習の違い
    - i.i.d（independent and identically distributed: 独立同分布）を仮定するか
        - 教師ありでは仮定している
    - 訓練データが受動的か能動的か
    - フィードバックが直接的か間接的か
- ニューラルネットワークの万能近似定理
- アーキテクチャ設計
    - 従来の機械学習では特徴抽出にドメイン知識を入れていた
    - 今ではアーキテクチャ設計時にドメイン知識を入れている
- 畳み込み層と全結合層の違い
    - 畳み込みの方が非常に疎な結合
        - 一方で、領域内では全ての入力とつながっている
    - 畳み込みは、位置が異なるシナプス間で同じ重みを共有している
        - 移動不変性を獲得
- プーリング
    - サイズを小さくしたり特定の周波数のみ切り出したり
- DL三大発明
    - ReLU
    - バッチ正則化
    - スキップ接続
- ReLU
    - 非線形
    - 値のスケール
    - 微分のスケール
        - 誤差がそのまま流れる
        - 誤差の消失や発散を抑える
- スキップ接続
    - 残差接続
    - 多層構成が可能に
    - Residual Network
    - 情報を落とさずボトルネックを使える
- 注意機構
    - 入力によって接続や重みが変わる
    - 注意：破壊的忘却（catastrophic forgetting）
        - 他のタスクを解く上で有用だったパラメータが壊れてしまう
    - 遠く離れた情報をワンステップで読み込める
- self-attention
    - O(N^2)が難点
    - 改良した Big Bird

### 分類問題でなぜクロスエントロピー損失
二乗誤差では、予測が真の値に近づくにつれて勾配の大きさが急激に０に近づく。一方、クロスエントロピー損失では、スコアの勾配が小さくなることはない(p87)。

経験分布とモデル分布間のKLダイバージェンスを最小化する関数を考えると、クロスエントロピー損失関数が登場し、これは観測データの歩の対数尤度と一致する。

### 正則化
学習時に、訓練誤差の最小化に加えて汎化性能を上げるために行う操作のこと。

- 目的関数をに正則化項を加える
    - パラメータのノルムのL2,L1を加えたり
- データオーギュメンテーション
