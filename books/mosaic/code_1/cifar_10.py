import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras.layers as layers

cifar_classes = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar10.load_data()
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

fig = plt.figure(figsize=(14,14))
for i in range(100):
    ax = plt.subplot(10, 10, i+1)
    ax.imshow(X_train[i])
    ax.axis("off")
    ax.set_title(cifar_classes[y_train[i, 0]])


