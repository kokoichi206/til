import kotlinx.coroutines.*

fun main() {
    class User4 {
        //    lateinit var name: String
        val isValidName: Boolean
            get() = name != ""  // getter の処理を書き換えている
        var name: String = ""
            set(value) {
                if (value == "") {
                    field = "Kotlin"
                } else {
                    field = value
                }
            }
    }

    demoo()
    test()
    chunkedTest()
    GlobalScope.launch {
        delay(1000L)
        println("Naoto.")
    }
    println("My name is")
    // これがないと、途中で関数が終わる！（メモリ的に安全になっている！）
    Thread.sleep(2000L)

    runBlockingTest()
    asyncTest()
}

// 関数型の定義
val calc: (Int, Int) -> Int = { num1: Int, num2: Int -> num1 + num2 }

// 引数が１つの時は、暗黙的に it が使われる
val squared: (Int) -> Int = { it * it }

fun checker() {
    println(calc(10, 5))
}

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

typealias Calc = (Int, Int) -> Int

fun printCalcResultByAlias(num1: Int, num2: Int, calc: Calc) {
    val result = calc(num1, num2)
    println(result)
}

// 拡張関数
fun Int.square(): Int = this * this

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

data class User(var id: Int = 0, var name: String)

fun scopeFunc(name: String?): User? {

    fun createUser(name: String?): User? {
        return name?.let { n -> User(name = n) }
    }

//    return if (name != null) User(name) else null
    return name?.let { n -> User(name = n) }
}

fun getUser(id: Int): User {
    return User(id = id, name = "default")
}

fun updateUser(id: Int, newName: String) {
    val user = getUser(3).apply {
        name = newName
    }
    println(user)
}

fun test() {
    println(Num(3) + Num(6))
    println(Num(4) + 3)
}

data class Num(val value: Int) {
    operator fun plus(num: Num): Num {
        return Num(value + num.value)
    }

    operator fun plus(num: Int): Num {
        return Num(value + num)
    }
}

fun chunkedTest() {
    val list = listOf(1, 2, 3, 4, 5, 6, 7)
    val chunckedList = list.chunked(2)
    println(chunckedList)
    chunckedList.forEach { println(it) }
}

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

