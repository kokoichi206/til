## 資料
- [github sample code](https://github.com/upura/python-kaggle-start-book)
- [catboost](https://catboost.ai/)
- [LightGBM Parameters](https://lightgbm.readthedocs.io/en/latest/Parameters.html)
- [時系列データセットの分割に関するスライド](https://www.slideshare.net/ShotaOkubo/neko-kin-96769953)

## sec 1

### Kaggle システム
- 順位表は「Leaderborad」と呼ばれ、Public Leaderboard と　Private Leaderboard に分かれる
- Private LB は、最終順位となる LB
  - コンペ終了時にのみ確認できる
- Public LB と Private LB に使われるテストデータの割合は、コンペによって異なる

## sec 2

### 特徴量エンジニアリング
- 読み込んだデータを機械学習アルゴリズムが扱える形に変換
- 既存のデータから、機械学習アルゴリズムが予測する上で有用な新しい特徴量を作成

```python
data = pd.concat([train, test], sort=False)
# 文字列を数値に変換
data['Sex'].replace(['male', 'female'], [0, 1], inplace=True)

# 欠損値を穴埋めしたりする
data['Fare'].fillna(np.mean(data['Fare']), inplace=True)
```

#### 疑問
- `inplace=True`は何か
  - pandas.DataFrame を変換後のものに置き換える！

### 欠損値の補完
- 欠損値としてそのまま扱う
- 代表的な値で欠損値を補完する
- 他の特徴量から欠損値を予測して補完する
- 欠損値か否かの情報を用いて新しい特徴量を作る

### train と test の結合
```python
data = pd.concat([train, test], sort=False)
```

この結合には、次のような利点がある！

- 共通する処理を train と test のそれぞれに実行する必要がなくなる
- test の情報も考慮した処理を実行できる
  - 平均値など？
  - 一方で業務では、モデル作成時に、予測対象のデータについて情報が得られない場合も多い。このような観点から、特徴量エンジニアリングの段階では test の情報を利用するのは好まない、という意見もある


### 探索的データ分析
Exploratory Data Analysis, EDA

２ステップ

1. データ把握
2. 仮説探し

#### Pandas Profiling
実行に時間がかかるので、大きいデータの場合は一部のデータに対して行う

#### カテゴリ変数
機械学習アルゴリズムは、数値ではない文字列を入力として扱えない場合が多い。

そのため特徴量エンジニアリングの段階で、カテゴリ変数を適当な数値に置き換える処理が必要となる


### 新しい特徴量を作る
再現性が大事

- 乱数を用いない方法にする
- 乱数の seed を固定する

```python
mport seaborn as sns


data['FamilySize'] = data['Parch'] + data['SibSp'] + 1
train['FamilySize'] = data['FamilySize'][:len(train)]
test['FamilySize'] = data['FamilySize'][len(train):]
sns.countplot(x='FamilySize', data = train, hue='Survived')
```

```python
data['IsAlone'] = 0
data.loc[data['FamilySize'] == 1, 'IsAlone'] = 1

train['IsAlone'] = data['IsAlone'][:len(train)]
test['IsAlone'] = data['IsAlone'][len(train):]
```

### いろいろな機械学習アルゴリズムを使ってみよう！
sklearn では、宣言するモデルを切り替えるだけで機械学習アルゴリズムを差し替えられる

```python
# from
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(penalty='l2', solver='sag', random_state=0)

# to
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
```

#### LightGBM

##### 事前準備
sklearn との差異もあり、いくつかの事前準備が必要

1. 学習用・検証用にデータセットを分割する
2. カテゴリ変数をリスト形式で宣言する

##### 特徴
- LightGBM は「決定木」をもとにした機械学習アルゴリズム
- LightGBM は勾配ブースティングと呼ばれる
- 過学週に陥る可能性が高いため、「early stopping」を利用するのが一般的
- カテゴリ変数に対して特別な処理を自動的に実行してくれる
  - 何をカテゴリ変数として扱ってほしいかを明示的に LightGBM に教える

```python
model = lgb.train(params, lgb_train,
    valid_sets=[lgb_train, lgb_eval],
    verbose_eval=10,    # 10 回改善が見られなければ打ち切り
    num_boost_round=1000,
    early_stopping_rounds=10)
```

### ハイパーパラメタの調整

#### LightGBM における調整
- 大きめの max_bin を使う
  - 学習を高速化するため、特徴量をヒストグラムに変換している
  - default: 255
- 小さめの learning_rate を使う
  - default 0.1
- 大きめの num_leaves を使う
  - default 31

```python
import lightgbm as lgb


lgb_train = lgb.Dataset(X_train, y_train,
                                         categorical_feature=categorical_features)
lgb_eval = lgb.Dataset(X_valid, y_valid, reference=lgb_train,
                                         categorical_feature=categorical_features)

params = {
    'objective': 'binary',
    'max_bin': 300,
    'learning_rate': 0.05,
    'num_leaves': 40
}

model = lgb.train(params, lgb_train,
                               valid_sets=[lgb_train, lgb_eval],
                               verbose_eval=10,
                               num_boost_round=1000,
                               early_stopping_rounds=10)

y_pred = model.predict(X_test, num_iteration=model.best_iteration)
```

#### チューニングツール
- Grid search
- Bayesian Optimization
- Hyperopt
- Optuna

いずれにせよ、ハイパーパラメータの正しい理解が必要！！(documentation や論文を読んでみる！)


### Cross Validation

#### 学習用データセットから検証用データセットを作る
ホールドアウト検証という、一種の validation

#### Cross Validation (CV)
学習用データセットを無駄にしない！という利点

常にスコアが上がるとは限らない

時系列性を意識した検証用データセット構築が必要な場合もある

```
sklearn -> KFold

fold,

oof (Out Of Fold)
```

### アンサンブル
- 複数の機械学習モデルを組み合わせることで性能の高い予測値を獲得する手法
- アンサンブルは基本的に、やればやるだけ伸びる
- seed averaging なども

#### 相関を調べる
アンサンブルの観点では多様性が大切。予測値の相関が小さい方が望ましい。

アンサンブルの文脈では 0.95 以下なら十分に相関が小さいと言えそう

```python
# ３つの csv (から pandas で読み取ったもの)を比較する
df = pd.DataFrame({'sub_lgbm_sk': sub_lgbm_sk['Survived'].values,
            'sub_lgbm_ho': sub_lgbm_ho['Survived'].values,
            'sub_rf': sub_rf['Survived'].values})
df.head()

df.corr()

# 多数決の要領
sub = pd.read_csv('../input/titanic/gender_submission.csv')
sub['Survived'] = sub_lgbm_sk['Survived'] + sub_lgbm_ho['Survived'] + sub_rf['Survived']
sub['Survived'] = (sub['Survived'] >= 2).astype(int)
sub.to_csv('submission_lightgbm_ensemble.csv', index=False)
sub.head()
```

## sec 3

### 複数テーブル
1 : N の関係のテーブルのお場合、何かしらの方法で集約する必要がある。

```python
previous_loan_counts = \
    bureau.groupby('SK_ID_CURR', as_index=False)['SK_ID_BUREAU'].count().rename(
        columns={'SK_ID_BUREAU': 'previous_loan_counts'})
previous_loan_counts.head()

application_train = \
    pd.merge(application_train, previous_loan_counts, on='SK_ID_CURR', how='left')

application_train['previous_loan_counts'].fillna(0, inplace=True)
application_train.head()
```

### 画像データ
- [Adversarial example](https://tech.preferred.jp/ja/blog/nips17-adversarial-learning-competition/)

### テキストデータ
NLP コンペ

## sec 4

### コンペにつけられることが多いタグ
- テーブルデータ
  - tabular data
- 画像データ
  - image data
- テキストデータ
  - nlp, text data

### Code Competitions
Code competitions は、Notebooks 環境を用いて submit するひつよグアあるタイプ。大きく２つのルールのタイプがある

- 特徴量の作成、学習、テストデータの予測など全ての処理を１つの Notebook に記述する必要があるコンペ
- テストデータを予測する処理を Notebook に記述する必要があり、特徴量の作成や学習は Notebook の外で行えるコンペ


## おことば
- 全部やる
  - 実際にどの技法が効果があるか、データセットや課題次第
    - 頭であれこれ議論するだけでなく、手を動かして全通りを確認しよう
- 仮説と可視化を繰り返すサイクルが大切
  - 予測性能に寄与しそうな仮説を立てる
  - 可視化を実行する
- ハイパーパラメータの調整よりは、特徴量エンジニアリングなどの方が大事
- Trust CV
  - Public LB のスコアよりも、自分で計算した CV のスコアを信じよう
