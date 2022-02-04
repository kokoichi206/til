## sec 1

### テスト手法
- ブラックボックステスト
    - 決められた操作や入力に対して期待通りの結果や出力が得られること
    - 外部から観測できる結果が仕様書に沿っていることが重要
    - 内部的にどのような実装かは考慮されない
- ホワイトボックステスト
    - プログラムの内部構造に着目し、処理や分岐が正しく行われていることを確認するテスト
    - 内部的なロジックのチェックに重きが置かれている
    - そのため、仕様を勘違いしていた場合、ホワイトボックステストとしては正しいがブラックボックステストとしては期待通りでないこともあり得る

### テスト種類
The Testing Pyramid

- Unit Test
    - 70%
- Integration Test
    - 20%
- UI Test
    - 10%

### UnitTest
- Local Unit Test
- Instrumented Unit Test
    - 実機やエミュレータを使ってユニットテストを実行する手法

### テストのメリット
- テストは動く仕様書
- 急がば回れ
    - テストを書いて少しずつ実行しながら漸進的に開発していくスタイルの方が各モジュールの開発状況の進展はわかりやすくなる
    - 日単位どころか時間単位で可視化されているので、より正確にプロジェクトの現況や着地点を予測することが可能
- テストは資産
    - てで実行したテストは費用、コードで記述され自動化されたテストは資産


## sec 2
Local Unit Test

Testing Framework を使う

### マッチャー
assertThat() メソッドは第二引数に「期待する状態がどのような状態か」を定義した**マッチャー**を指定する

Hamcrest は JUnit4 に標準で組み込まれている

``` kotlin
assertThat(1+1, `is`(2))
assertThat(100, greaterThan(50))
assertThat(listOf("for", "bar", "baz), hasItem("bar"))
```

- [コマンドラインからテストの実行](https://developer.android.com/studio/test/command-line?hl=ja)
- [テストメソッド命名](https://developer.android.com/training/testing/unit-testing/local-unit-tests?hl=ja#kotlin)
    - この辺参考になると思う


### テストケースを減らすためのテクニック
費用対効果の高いテストケースを意識する

- 同値分類
    - テスト対象が同じ挙動をする値を一つの群と考えて値をグループ分けする
    - 同値クラスからの代表値の選別
- 境界値
- 単項目チェック
    - ビジネスロジックでは複数の条件を組み合わせて成り立つことが一般的だが、ある１つの条件をみると、その結果によっては全て結果が決まるものがある。

> ユニットテストは完璧ではない。ホワイトボックステスト自体がそもそもロジックのわかる実装者がある程度内部実装を意識しつつ描くものであり、考慮漏れ自体は避けられない。ユニットテストをバグ発生の護符と捉えるより、部分的に実行可能な仕様書兼成果物くらいに考えておく


### AssertJ
Hamcrest よりもさらに自然言語に近く読みやすいアサーションを提供

### 次世代アサーションライブラリの覇者は？
Truth は AssertJ に似たインターフェイスを持ち、読みやすく、Kotlin との相性も良いことから最有力候補のひとつ

### テストダブル
テスト対象が依存しているコンポーネントを「本物そっくりに振る舞い影武者（ダブル）」と差し替えることで、自分の期待する挙動や値の返却を達成するテクニック。

テストダブルには５つの役割が定義されている

- スタブ
    - 事前定義した任意の値をテスト対象に与える
- モック
    - テスト対象が依存コンポーネントに与える値や挙動を検証する
- スパイ
    - スタブの上位互換
- フェイク
    - 実際のコンポーネントと同等か極めてそれに近い挙動を持つ実装オブジェクト
- ダミー

### スタブ
- StubSatellite
- 元クラスを override
- テスト対象の入力を任意にコントロールする

### モック
- MockSatellite
- 元クラスを override
- メソッドが呼び出されたことや、メソッドに渡された引数をチェック
- **依存コンポーネントに与える値（出力）の検証**

### スパイ
- スタブの上位互換？
- テスト対象に値を与えるのが主な責務
- また、モックと同じくテスト対象が依存コンポーネントに与える値を記録する機能も
- テスト対象に与える値(入力)のコントロール！

> 「スタブのテスト」にならないように注意する。外界とのやり取りの有無で考えると良いかも

### Mockito でテストダブルを便利に扱う
依存コンポーネント全てでテストダブルを自ら用意するのは現実的ではない！

実際の開発現場では、テストダブルを便利に扱うためのライブラリ、**モックライブラリ**を使用するのがほとんど。

Mockito を使うと簡単に依存コンポーネントのモックを作ってテスト対象とのやりとりを検証したり、メソッド呼び出しをスタブ化したりして戻り値をコントロールできる。

ただ、一部の機能が Kotlin と相性が良くない。。（Mockito.when(), Mockito.any()）

-> Mockito-Kotlin:

``` kotlin
import com.nhaarman.mockitokotlin2

// name をつけるとエラーメッセージが分かりやすくなる
val satellite: Sattellite = mock(name="MockSatellite")
// or
val satellite = mock<Sattellite>(name="MockSatellite")
```

引数マッチャー

``` kotlin
val satellite: Satellite = mock(name="MockSatellite")
whenever(satellite.getWeather(any(), any()))
    .thenReturn(Weather.CLOUDY)
whenever(satellite.getWeather(eq(37.580006), eq(-122.345106)))
    .thenReturn(Weather.SUNNY)

whenever(satellite.getWeather(any(), any()))
    .thenAnswer { invocation ->
        val latitude = invocation.arguments[0] as Double
        val longitude = invocation.arguments[1] as Double

        if (latitude in 20.33..45.55 &&
            longitude in 122.93..153.98) {
            return@thenAnswer Weather.SUNNY
        } else {
            return@thenAnswer Weather.RAINY
        }
    }
```

thenAnswer{} はラムダ式なので、中から直接 return することができない。よって、return@thenAnswer でラムダ式から抜けるようにしている！！

呼び出しのチェック

``` kotlin
val recorder = mock<WeatherRecorder>(name="hoge")
// 引数も検証できる
verify(recorder, times(1)).record(eq("Weather is SUNNY"))
```

### 新しいモックライブラリ MockK
Kotlin のために１から書かれた新しいモックライブラリ。Kotlin のコルーチンや拡張関数のモックにも対応するなど、大きな可能性を秘めている。













## 命名
- isValid_givenAlphaNumeric_returnsTrue()
- isEqualToIgnoringCase

