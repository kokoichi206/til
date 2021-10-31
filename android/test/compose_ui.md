## [Youtube(Social Network)](https://www.youtube.com/watch?v=POfR2BA3Ljk&ab_channel=PhilippLackner)
- Navigation should be tested by mock


### testTag
Composable の testTag は、テストのためだけにある

ソースコードっは少し汚くなるけど、そうしないと見つけられない。

modifier : Modifier = Modifier として、テストの時だけ、tag のついた modifier を渡す、という方法もあることにはある

### Access to context
```kotlin
ApplicationProvider.getApplicationContext<Context>()
```


### Coroutine
@ExperimentalCoroutinesApi

runBlockingTest, coroutine などを待たない？ delay(5000) などを待たずに実行する？

```kotlin
this.advanceTimeBy(Constants.SPLASH_SCREEN_DURATION)
```


### Search
- Android ui test example
- jetpoack compose test launched effect
- jetpack compose launched effect swap out scope


### MVVM
- usecase: domain package
- viewmodel: presentation package

### Others
- Timber
  - usuful logger

### パスワードの切り替え
```kotlin
visualTransformation = if (isPasswordToggleDisplayed) {
    PasswordVisualTransformation()
} else {
    VisualTransformation.None
},
```

### semantics
テストの時だけ　tag をつけられるように、StandardTextField のコンストラクタとして、modifier を渡すように変更

semantics の方が好みらしい、使えない時はどんな時？？

```kotlin
modifier = Modifier.semantics { 
    contentDescription = text
}
```


## English
Let's ask google.

current meeting running late, 2min

On second thought, you might be right.

