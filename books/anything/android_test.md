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


## sec 3

### Robolectric
Local Unit Test ではモジュールに android.* の名前空間のクラス群が含まれる場合、Android SDK によって提供される android.jar でフレームワークの依存関係を解決する。ただ、これはあくまで名前解決の便宜上提供されているダミーに過ぎず、実機やエミュレータ以外で実行しようとすると実行時例外が上がってテストが失敗する。

そこで、「フレームワークのモック」が簡単に行える Robolectric を使う

Robolectric は Android フレームワークのコードをシミュレートして JVM 上で高速に実行できるテストフレームワーク

### SQLite を利用したモジュールの Test
Robolectric は **shadow** と呼ばれる仕組みを使って Android フレームワークのコードをシミュレートする。

Jetpack ファミリーのひとつであり、柔軟なオブジェクトマッピングを提供する SQLite のラッパーライブラリ Room Persistence Libracy を使ってみる

### 非同期処理のユニットテスト
- 非同期処理はコールバック関数を通じて処理の完了を通知してもらうことが多いので戻り値を返さず検証がしづらい
- 非同期処理では呼び出し元スレッドと実行スレッドが異なるため、実行順序を考える必要があるなど検証が容易ではない

``` kotlin
class StringFetcher {
    fun fetch(): String {
        Thread.sleep(1000L)
        return "foo"
    }
}
```

StringFetcher を利用して非同期に処理を実行し、結果をコールバックとして返すための AsyncStringFetcher クラス！

``` kotlin
class AsyncStringFetcher(val fetcher: StringFetcher) {
    val executor: ExecutorService = Executors.newCachedThreadPool()

    fun fetchAsync(onSuccess: (value: String) -> Unit,
                onFailure: (error: Throwable) -> Unit) {
        executor.submit {
            try {
                val value = fetcher.fetch()
                onSuccess(value)
            } catch (error: Throwable) {
                onFailure(error)
            }
        }
    }
}
```


### OkHttp と Retrofit を使ったモジュールのユニットテスト
OkHttp は決済大手の Square 社が中心となって開発している OSS の HTTP クライアント。標準で HTTP/2 やレスポンスキャッシュなどをサポートし、シンプルかつ柔軟な使い勝手から Android における HTTP クライアントとしてデファクト。

Retrofit は同じく Square 社の OSS で、REST クライアントを作成する際のボイラープレートを大幅に削減してくれるライブラリ。HTTP 通信部分は標準で OkHttp を利用する。

Retrofit と OkHttp の組み合わせは Android で REST 通信をする際の強力な選択肢になる


### MockWebServer

### MVP architecture
一般に、**Fat Controller**（コントローラの責務過多）問題がある。この問題に対処するためにさまざまな多層アーキテクチャが生み出されている。

今回はそのうちの MVP アーキテクチャに注目する

- Model layer
    - データ構造及びデータを操作する処理群
- View layer
    - UI 部品の操作
- Presenter layer
    - 両者の橋渡し

#### モデル層
モデル層の実装方法としてユースケースやリポジトリパターンなど様々ある。本項では取得したいデータを RxJava の Single でラップして返すリポジトリを想定している

``` kotlin
class GitHubRepository(val localDataSource: LocalDataSource) {
    fun listRepos
}
```

#### View と Presenter
Activity は View と Controller の中間のような存在にあるため、View と Presenter の責務を分けにくい。

ここでは、View = Activity or Fragment と定義し、これは賢いロジックを持たず「Presenter の求めに応じて UI 部品を更新する層」と定義する

Activity はライフサイクルを持ち、UI コンポーネントを直接扱うことから android.* 名前空間と切っても切れない存在なので、そのままでは Local Unit Test が困難。

従って、View と Presenter が互いに果たす責務をシンプルなインターフェイスとして定義する

``` kotlin
interface View {
    fun showRepositoryList(list: List<Repo>)
}

interface Presenter {
    fun getRepositoryList(name: String)
}
```

これを踏まえて Activity を実装する

``` kotlin
class MainActivity: AppCompatActivity(), View {
    override fun showRepositoryList(list: List<Repo>) {

    }

    override fun onCreate(savedInstanceState: Bunde?) {
        val repository = GitHubRepository(LocalDataSource())
        val presenter = ListPresenter(this, repository)
        presenter.getRepositoryList("kokoichi")
    }
}
```

``` kotlin
class ListPresenter(val view: View,
                val repository: GitHubRepository) : Presenter {
    override fun getRepositoryList(name: String) {
        repository.listRepos(name)
            .subscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
            .subscribeBy { view.showRepositoryList(it) }
    }
}
```

1. 注目すべきはコールバック相手の View の参照を Activity それ自体ではなく、View インターフェイス型としてもらっているてん。こうすることでユニットテストを書く際に Activity を直接扱わなくてもすむ。
1. Presenter#getRepositoryList() が呼び出されるとモデル層の GitHubRepository#listRepos() に処理を移譲する
1. データ取得後は subscribeBy { view.showRepositoryList(it) } のように View に対して結果をコールバックする。まさに橋渡し役


### テストのないプロジェクトにテストを導入する
データを取得するモジュールが Local..., Remote... ともにフィールドに private 宣言されており、テストダブルに置き換えることが困難。

static メソッドに関しては上書きできないため動作の確認がめんどくさい

アクセス権を private にしたままスタブに差し替えるには、Mockito の InjectMocks アノテーションを利用できる

ただ、InjectMocks は final なフィールドをモックで差し替えることができない。**Kotlin ではデフォルトで final になる**ので、var で変数定義する必要があるが、テストのためにするのは不恰好すぎる。

そこで、**依存関係をコンストラクタから渡してしまうというアプローチ**が有効なことも！












## 命名
- isValid_givenAlphaNumeric_returnsTrue()
- isEqualToIgnoringCase
- isValid_givenBlank_throwsIllegalArgumentException()

