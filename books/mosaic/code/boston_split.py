from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)
print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)

inputs = layers.Input((13,))
x = layers.Dense(1)(inputs)
model = tf.keras.models.Model(inputs, x)
model.compile("adam", "mean_squared_error")

### model.fit(訓練データのX, 訓練データのy, validation_data=(テストデータのX, テストデータのy), epochs=エポック数)
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10)
###

