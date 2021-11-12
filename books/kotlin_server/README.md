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


### sec 2 : さまざまな Kotlin の機能
- if, when を式としてうまく使う
- 内部的に getter, setter がある
  - val の定義では getter のみ生成される！
- lateinit の値が getter 呼び込み時に格納されているかは、コンパイル時に検知できない！
  - **より注意して扱う！**
- データクラスを使うことでボイラープレートを減らせる
  - 全てのクラスは Any というクラスを継承している
    - toString, hashCode, equals の３つが定義されている
  - data class では、以下の関数をよくしてくれている
    - アクセスメソッド
    - equals
    - hashCode
    - toString
    - componentN
    - copy
- 関数リテラル
  - 関数を値として記述するもの
  - 無名関数、ラムダ式
- タイプエイリアス
- 拡張関数
  - 柔軟にロジックを追加できる！
- スコープ関数
  - with, run, let, apply, also
- 演算子オーバーロード
  - operator
- [collections](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/)
  - forEach, map, filter, first, last, firstOrNull, lastOrNull, distinct, chunked


#### 関数リテラル
```kotlin
// 関数型の定義
val calc: (Int, Int) -> Int = { num1: Int, num2: Int -> num1 + num2 }
// 引数が１つの時は、暗黙的に it が使われる
val squared: (Int) -> Int = { it * it }
```

#### 高階関数
```kotlin
// 高階関数
fun printCalcResult(num1: Int, num2: Int, calc: (Int, Int) -> Int) {
    val result = calc(num1, num2)
    println(result)
}

// ----------- usage -----------
fun demo() {
    printCalcResult(10, 20) { num1, num2 -> num1 + num2 }
    printCalcResult(10, 20, { num1, num2 -> num1 + num2 })
    printCalcResult(10, 20) { num1, num2 -> num1 * num2 }
}
```

#### タイプエイリアス
```kotlin
typealias Calc = (Int, Int) -> Int
fun printCalcResultByAlias(num1: Int, num2: Int, calc: Calc) {
    val result = calc(num1, num2)
    println(result)
}
```

#### 拡張関数で柔軟にロジックを追加できる！
```kotlin
fun demoo() {
    class MyNumber(val num: Int, val name: String = "name") {
    }
    val n1 = MyNumber(3)
    // 後からメソッド等ロジックを追加できる（テスト時に使えそう？）
    fun MyNumber.square(): Int = this.num * this.num
    println(n1.square())

    // Int 等にも拡張できる
    fun Int.square(): Int = this * this
    println(4.square())
}
```

#### スコープ関数
let - Nullable なオブジェクトに名前をつけて処理を行う

`if (name != null)`は let のよく使われる場面！

```kotlin
data class User(val name: String)
fun scopeFunc(name: String?): User? {

    fun createUser(name: String?): User? {
        return name?.let { n -> User(n) }
    }

//    return if (name != null) User(name) else null
    return name?.let { n -> User(n) }
}
```

apply は、レシーバオブジェクト自体を返す

```kotlin
fun updateUser(id: Int, newName: String) {
    val user = getUser(3).apply {
        name = newName
    }
    println(user)
}
```

also は、オブジェクトに変更を加えて返す（名前付き）

#### 演算子オーバーロード
plus, minus, times, div, compareTo,.. などが対象

```kotlin
fun test() {
    println(Num(3) + Num(6))
    println(Num(4) + 3)
}
// data クラスに対して定義する感じかな
data class Num(val value: Int) {
    operator fun plus(num: Num): Num {
        return Num(value + num.value)
    }
    operator fun plus(num: Int): Num {
        return Num(value + num)
    }
}
```

#### chunked
```kotlin
fun chunkedTest() {
    val list = listOf(1, 2, 3, 4, 5, 6, 7)
    val chunckedList = list.chunked(2)
    println(chunckedList)
    chunckedList.forEach { println(it) }
}
// [[1, 2], [3, 4], [5, 6], [7]]
// [1, 2]
// [3, 4]
// [5, 6]
// [7]
```

#### reduce
```kotlin
val list = listOf(1, 2, 3, 4, 5)
val result = list.reduce { sum, value -> sum * value }  // 120
```

#### コルーチン
- コルーチンスコープ: GlobalScope など
- コルーチンビルダー: launch など

- runBlocking: コルーチンビルダーに当たる関数
  - スコープ内の子ルーチンの処理が全て終わるまで終了しないようにスレッドをブロックする！
- async: コルーチンビルダー**の**関数
  - launch と似ているが async はラムダ式で描いた処理の結果の値を受け取ることができる


```kotlin
fun runBlockingTest() {
    runBlocking {
        launch {
            delay(1000L)
            println("Hogeo")
        }
        println("my name issss")
    }
}

fun asyncTest() {
    runBlocking {
        val result = async {
            delay(2000L)
            var sum = 0
            for (i in 1..100) {
                sum += i
            }
            sum
        }
        println("計算中")
        println("sum=${result.await()}")
    }
}
```

