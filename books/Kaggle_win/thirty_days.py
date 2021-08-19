from xgboost import XGBRegressor
import itertools
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error

# my_model = XGBRegressor()
# my_model.fit(X_train, y_train)
param_space = {
    'max_depth': [3, 5, 7],
    'min_child_weight': [1.0, 2.0, 3.0]
}

# 探索するハイパーパラメータの組み合わせ
param_combinations = itertools.product(param_space['max_depth'], param_space["min_child_weight"])

# 各パラメータの組み合わせ、それに対するスコアを保存するリスト
params = []
scores = []

# トレーニングに使う特徴りょう
train_x = X
# トレーニングに使う目的変数
train_y = y

# 進捗表示用
num_params = len(param_combinations)
now = 0
import datetime
dt_now = datetime.datetime.now()
print(dt_now)

for max_depth, min_child_weight in param_combinations:
    
    score_folds = []
    # クロスバリデーションを行う
    kf = KFold(n_splits=4, shuffle=True, random_state=123456)
    for tr_idx, va_idx in kf.split(train_x):
        tr_x, va_x = train_x.iloc[tr_idx], train_x.iloc[va_idx]
        tr_y, va_y = train_y.iloc[tr_idx], train_y.iloc[va_idx]
        
        # モデルの学習を行う
        model = XGBRegressor(n_estimators=1000, random_state=71,
                            max_depth=max_depth, min_child_weight=min_child_weight)
        model.fit(tr_x, tr_y)
        
        # バリデーションデータでのスコアを計算し、保存する
        va_pred = model.predict(va_x)
        logloss = mean_squared_error(va_y, va_pred)
        score_folds.append(logloss)
        
    # 各foldのスコアを平均する
    score_mean = np.mean(score_folds)
    
    # パラメータの組み合わせ、それに対するスコアを保存
    params.append((max_depth, min_child_weight))
    scores.append(score_mean)
    
    # 進捗を表示
    now += 1
    print_str = str(dt_now) + '- [' + '■'*now + ' '*(num_params-now) + ']'
    print(print_str)

print(params)
print(scores)

# もっともスコアが良いものを取る
best_idx = np.argsort(scores)[0]
best_param = params[best_idx]
print(f'max_depth: {best_param[0]}, min_child_weight: {best_param[1]}')
