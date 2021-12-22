import tensorflow.keras.layers as layers

### layers.Conv2D(チャンネル数, カーネルサイズ, padding="same")(入力)

import tensorflow as tf
import tensorflow.keras.layers as layers

inputs = layers.Input((32,32,3))
x = layers.Conv2D(64, 3, padding="same")(inputs)
x = layers.BatchNormalization()(x)
x = layers.ReLU()(x)
model = tf.keras.models.Model(inputs, x)
###
model.summary()

### Pooling
inputs = layers.Input((32,32,3))
x = layers.AveragePooling2D(2)(inputs)

model = tf.keras.models.Model(inputs, x)
###
model.summary()


# Conv層とPooling層をあわせて、3つの畳み込み層からなるモデルを作る。具体的には、
# Conv 64ch -> BN -> ReLU -> Pooling
# Conv 128ch -> BN -> ReLU -> Pooling
# Conv 256ch -> BN -> ReLU
inputs = layers.Input((32,32,3))
## １層目
x = layers.Conv2D(64, 3, padding="same")(inputs)
x = layers.BatchNormalization()(x)
x = layers.ReLU()(x)
x = layers.AveragePooling2D(2)(x)
## 2層目
x = layers.Conv2D(128, 3, padding="same")(x)
x = layers.BatchNormalization()(x)
x = layers.ReLU()(x)
x = layers.AveragePooling2D(2)(x)
## 3層目
x = layers.Conv2D(256, 3, padding="same")(x)
x = layers.BatchNormalization()(x)
x = layers.ReLU()(x)

model = tf.keras.models.Model(inputs, x)
###
model.summary()

## Global Average Pooling
inputs = layers.Input((8,8,256))
x = layers.GlobalAveragePooling2D()(inputs)
x = layers.Dense(10, activation="softmax")(x)
model = tf.keras.models.Model(inputs, x)
##
model.summary()


### Model for cifar-10
inputs = layers.Input((32,32,3))
x = inputs
for ch in [1, 2, 4]:
    for i in range(3):
        x = layers.Conv2D(64*ch, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
    if ch != 4:
        x = layers.AveragePooling2D()(x)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(10, activation="softmax")(x)

model = tf.keras.models.Model(inputs, x)
###
model.summary()


### 訓練のための下準備
X_train = X_train.astype(np.float32) / 255.0
X_test = X_test.astype(np.float32) / 255.0
y_train = y_train.astype(np.float32)
y_test = y_test.astype(np.float32)

model.compile("adam", "sparse_categorical_crossentropy", ["sparse_categorical_accuracy"])

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=128)

fig = plt.figure(figsize=(14,14))
y_pred = np.argmax(model.predict(X_test), axis=-1) # argmaxで予測ラベル

for i in range(100):
    ax = fig.add_subplot(10, 10, i+1)
    ax.imshow(X_test[i])
    ax.axis("off")
    if y_pred[i] == y_test[i,0]:
        ax.set_title(cifar_classes[y_pred[i]])
    else:
        ax.set_title(cifar_classes[y_pred[i]]+" / "+cifar_classes[int(y_test[i,0])], color="red")    

