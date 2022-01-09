from sklearn.datasets import load_boston
data = load_boston()
# print(data)

print(type(data))
print(data.keys())
print(data.feature_names)
print(data.data.shape, data.target.shape)
X = data.data
y = data.target
### <class 'sklearn.utils.Bunch'>
### dict_keys(['data', 'target', 'feature_names', 'DESCR', 'filename', 'data_module'])
### ['CRIM' 'ZN' 'INDUS' 'CHAS' 'NOX' 'RM' 'AGE' 'DIS' 'RAD' 'TAX' 'PTRATIO' 'B' 'LSTAT']
### (506, 13) (506,)

import tensorflow as tf
import tensorflow.keras.layers as layers

### 入力層の def 
inputs = layers.Input((13, ))
###
print(inputs)
# KerasTensor(type_spec=TensorSpec(shape=(None, 13), dtype=tf.float32, name='input_1'), name='input_1', description="created by layer 'input_1'")

### layers.Dense(出力次元)(前の層の変数)
outputs = layers.Dense(1)(inputs)
###
print(outputs)

model = tf.keras.models.Model(inputs, outputs)
###
print(model)
print(model.summary())

### model.compile(オプティマイザー, 損失関数)
model.compile("adam", "mean_squared_error")
###
print(model)

### model の訓練
model.fit(X, y, epochs=10)
###
y_pred = model.predict(X)
###
print(y_pred[:10])
print(y[:10])

### BatchNormalization を入れて収束を早くすることもできる
# inputs = layers.Input(13)
# x = layers.BatchNormalization()(inputs)
# x = layers.Dense(1)(x)
# model = tf.keras.models.Model(inputs, x)
# model.compile("adam", "mean_squared_error")
# model.fit(X, y, epochs=10)
### =========================
