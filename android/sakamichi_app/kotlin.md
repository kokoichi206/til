## sealed classes
[youtube](https://www.youtube.com/watch?v=qzzkui-Z6CM&t=28s&ab_channel=PhilippLackner)

sealed class と enum は共通点多いが、その違いについて

### Generic type

### usage
```kotlin
data class Person(
    val name: Stirng,
    val gender: Gender = Gender.Female
) {
    sealed class Gender {
        object Male: Gender()
        object Female: Gender()
        ...
    }
}
```



## 疑問
- object -> singleton class ?



## Colors
```kotlin
Log.d("test", "=========================================")
val color = Color(Random.nextInt(256), Random.nextInt(256), Random.nextInt(256))
Log.d("test", color.toString())
```

