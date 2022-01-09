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


## かっこいいいいねボタン
```kotlin
IconToggleButton(
    modifier = Modifier
        .align(Alignment.CenterEnd),
    checked = isChecked,
    onCheckedChange = {
        viewModel.toggleIsSortTime()
    },
) {

    val transition = updateTransition(isChecked, label = "Checked indicator")

    val tint by transition.animateColor(
        label = "Tint"
    ) { isChecked ->
        if (isChecked) Color.Red else Color.Black
    }

    Icon(
        imageVector = if (isChecked) Icons.Filled.Favorite else Icons.Filled.FavoriteBorder,
        contentDescription = null,
        tint = tint,
        modifier = Modifier.size(30.dp)
    )
}
```


## UseCase
- Make your business logic reusable.

