import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import optuna
from sklearn.metrics import mean_absolute_error


# import data
train = pd.read_csv('../input/ventilator-pressure-prediction/train.csv')
test = pd.read_csv('../input/ventilator-pressure-prediction/test.csv')
sample_submission = pd.read_csv('../input/ventilator-pressure-prediction/sample_submission.csv')

data = pd.concat([train, test], sort=False)

# prepare data
y_train = train['pressure']
X_train = train.drop('pressure', axis=1)
# X_test = test.drop('pressure', axis=1)
X_test = test


# separate data
X_train, X_valid, y_train, y_valid = \
    train_test_split(X_train, y_train, test_size=0.3,
                                 random_state=0, stratify=y_train)


# categorical_features = ['Embarked', 'Pclass', 'Sex']
categorical_features = []



def objective(trial):
    params = {
        'objective': 'binary',
        'max_bin': trial.suggest_int('max_bin', 255, 500),
        'learning_rate': 0.05,
        'num_leaves': trial.suggest_int('num_leaves', 32, 128),
    }
    
    lgb_train = lgb.Dataset(X_train, y_train,
                                         categorical_feature=categorical_features)
    lgb_eval = lgb.Dataset(X_valid, y_valid, reference=lgb_train,
                                         categorical_feature=categorical_features)

    model = lgb.train(params, lgb_train,
                                   valid_sets=[lgb_train, lgb_eval],
                                   verbose_eval=10,
                                   num_boost_round=1000,
                                   early_stopping_rounds=10)

    y_pred_valid = model.predict(X_valid, num_iteration=model.best_iteration)
    score = mean_absolute_error(y_valid, y_pred_valid)
    return score

study = optuna.create_study(sampler=optuna.samplers.RandomSampler(seed=0))
study.optimize(objective, n_trials=40)
study.best_params

params = {
    'objective': 'regression',
    'max_bin': study.best_params['max_bin'],
    'learning_rate': 0.05,
    'num_leaves': study.best_params['num_leaves']
}
​
lgb_train = lgb.Dataset(X_train, y_train,
                                         categorical_feature=categorical_features)
lgb_eval = lgb.Dataset(X_valid, y_valid, reference=lgb_train,
                                         categorical_feature=categorical_features)
​
model = lgb.train(params, lgb_train,
                               valid_sets=[lgb_train, lgb_eval],
                               verbose_eval=10,
                               num_boost_round=1000,
                               early_stopping_rounds=10)
​
y_pred = model.predict(X_test, num_iteration=model.best_iteration)

sample_submission['pressure'] = y_pred
sample_submission.to_csv('submission_optuna.csv', index=False)

sample_submission.head()

