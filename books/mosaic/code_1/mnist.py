import tensorflow as tf
import tensorflow.keras.layers as layers


(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
###
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)


### 手書き画像を表示
# import matplotlib.pyplot as plt
# fig = plt.figure(figsize=(14, 14))
# for i in range(100):
#     ax = fig.add_subplot(10, 10, i+1)
#     ax.imshow(X_train[i], cmap="gray")
#     ax.set_title(y_train[i])
#     ax.axis("off")

print(X_train[0])
###

inputs = layers.Input((28,28))
x = layers.Flatten()(inputs) # (28,28) -> (784,)に変形するための操作
x = layers.BatchNormalization()(x) # BatchNormでスケール調整
### ここにコードを入力
x = layers.Dense(128, activation="relu")(x)
x = layers.Dense(10, activation="softmax")(x)
model = tf.keras.models.Model(inputs, x)
###
print(model.summary())

model.compile("adam", "sparse_categorical_crossentropy", ["sparse_categorical_accuracy"])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10)
###

import numpy as np
### ここにコードを入力
y_pred_prob = model.predict(X_test)
###
y_pred = np.argmax(y_pred_prob, axis=-1)
print(y_pred_prob.shape, y_pred.shape)

### 予測
# fig = plt.figure(figsize=(14, 14))
# for i in range(100):
#     ax = fig.add_subplot(10, 10, i+1)
#     ax.imshow(X_test[i], cmap="gray")
#     ax.set_title(y_pred[i])
#     ax.axis("off")

