## Kotlin サーバーサイドプログラミング

[サンプルコード](https://github.com/n-takehata/kotlin-server-side-programming-practice)

### sec 1

#### Kotlin 
- JetBrains 社が開発した言語, 2016年2月に 1.0 がリリース
- JVM 言語の一種
- Java との相互運用ができる
- 2019, google, android Kotlin ファースト

#### サーバーサイドでの利用意義
通常は Web アプリケーションのバックエンド

#### Null 安全
- 型レベルで Null 非許容/許容を明示し、コンパイルでチェックしてくれる
  - エンジニアが自身で Null の扱いを強く意識しなくてよくなるため、開発効率も向上する

エルビス演算子：null の時のみ実行される

```kotlin
fun printMessageLength3(message: String?) {
    message ?: return   // null の時のみ実行される
    println(message.length)
}
```

**安全呼び出し**

```kotlin
fun printMessageLength(message: String?) {
    println(message?.length)
}
printMessageLength("Kotlin")  // 6
printMessageLength(null)      // null
// ? null の場合は null を返す！
```

**強制アンラップ**

```kotlin
// null が入ってた場合は実行時エラーとなるため、あんまり望ましくはない
fun printMessageLength(message: String?) {
    println(message!!.length)
}
```

