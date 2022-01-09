fun main() {

}

fun checkNum(num: Int) : Unit {
    when {
        num < 100 -> {
            println("Less than 100")
        }
        num == 100 -> {
            println("Equal to 100")
        }
        else -> {
            println("Greater than 100")
        }
    }
}

val map: Map<Int, String> = mapOf(
    1 to "one",
    2 to "two",
    3 to "three",
)
fun checkMap() {
    println(map.containsKey(3))
    println(map.containsKey(4))
}
