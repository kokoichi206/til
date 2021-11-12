## Kotlin サーバーサイドプログラミング

[サンプルコード](https://github.com/n-takehata/kotlin-server-side-programming-practice)

[自分のコード](./untitled/src)

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

#### build.gradle.kts　について
Gradle（ビルドツール）の設定ファイルを、Kotlin DSL という Kotlin で記述できるようにしたもの

#### 型
- Unit は何もないことを表す型、基本的には不要
  - void ?

####　シールドクラス
- 継承を制限する機能
- 継承・オーバーライドさせたい関数に関しては、open をつけておく必要がある
- seald をつけることで、このクラスは**他ファイルのクラスから**継承できなくなる

```kotlin
// 同一ファイル内からなら可能
seald class Platform {
    abstract fun showName()
}

class AndroidPlatform: Platform() {
    override fun showName() {
        println("Android.")
    }
}
class IosPlatform: Platform() {
    override fun showName() {
        println("iOS.")
    }
}
```

#### interface
- 継承のさせ方が微妙に違う？
  - クラスの場合は、() が着くけど、インターフェースの場合はつかない？

```kotlin
interface Greeter {
    fun hello()
}

// ------------- //
class GreeterImpl: Greeter {
    override fun hello() {
        println("Hello.")
    }
}
```

#### コレクション
- List
- Map
- Set


