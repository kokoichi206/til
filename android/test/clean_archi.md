## [youtube(The Ultimate Guide to Android Testing)](https://www.youtube.com/watch?v=nDCCwyS0_MQ&ab_channel=PhilippLackner)

### DB のテスト（今回は use_case）
DB アクセスを実際に行うわけにはいかないので、FakeXXXRepository を用意する

#### FakeRepository
list で構成されていて、動きだけをまねる

GetNotes のコンストラクトの引数を、Interface にしていたことで、mock(fake) を GetNotes に入れることができる！

### UI test
use hilt to inject our dependencies, because these test can be often involved some dependencies

### DB
```kotlin
// 普通
Room.databaseBuilder
// テスト用
Room.inMemoryDatabaseBuilder
```

#### di Module を変える？？

##### AppModule を uninstall する

```kotlin
@HiltAndroidTest
@UninstallModules(AppModule::class)
class NotesScreenTest {
}
```

##### Test 用の runner を用意する
```kotlin
class HiltTestRunner : AndroidJUnitRunner() {

    override fun newApplication(
        cl: ClassLoader?,
        className: String?,
        context: Context?
    ): Application {
        return super.newApplication(cl, HiltTestApplication::class.java.name, context)
    }
}
```

##### build.gradle の中の Runner を変更する
```
testInstrumentationRunner "io.kokoichi.sample.cleanarchitecture.HiltTestRunner"
```

### memo
get:Rule の順番を制御する

```kotlin
@get:Rule(order = 1)
```


