## MVVM 

### 全体の流れ
0. initial として、色とかを定義しておく
1. hilt を入れる
  1. HiltAndroid...
  2. di
2. api を作る
  1. data-remote とかを作る
  2. remote の中で、response, PokeApi wお作る
  3. repository パッケージを data の横に並べる
  4. repository を、記述する(util.Resource で囲む)
  5. di に記述
3. UI の記述を進める
4. ViewModel を作る
  1. data/models のなかに、Entry を作る
  2. 

### CAUTION
- USECASE は、常に１つの public function しか使わないようにする


FakeRepository でのテストが容易！やる！

they are directory coppuled to our presentations

Flow? resource values over time

### memo
押されたタイミングの値を、次の Composale で使いたいとかなら、次のような bundle の値を渡すのでもよき

```kotlin
private val savedStateHandle: SavedStateHandle,
```



