## カプセル化
- インスタンス変数は全て private にすることを目標とし、必要な場合にアクセさメソッドを用意する
- final 修飾子を使うことにより、メソッドがオーバーライドされないことを直接的に示しており、これによりこのメソッドを高速化できる。
  - → インライン化による、パフォーマンスとカプセル化の実現！！
  - メソッドを「インライン化」する場合には、コンパイラは該当のメソッド呼び出しが書かれている箇所に、そのメソッドの本体を展開する！
- インスタンス変数に対するアクセサメソッドは"final"にする！
- 注意しないと、継承はカプセル化を損なう
- 複雑さに対処するために、必ずパッケージを使う
- AWT: Abstract Windowing Tools

## 継承
- コンストラクタは継承されない
- 継承が有効かどうかをチェックする
  - "is a type of" という言葉が浮かべば、継承の可能性がある。
- 汎化
  - 共通のフィールドや振る舞いをくくり出すこと
- すべてのクラスは暗黙的にクラス Object を extends する
- 不要なキャストは避ける
- interface
  - メソッドのシグネチャ（操作）
  - static final なフィールド（名前付き定数）
- final クラス
  - 継承を禁ずる
  - abstract と対極
  - 型に安全な定数

## ポリモルフィズム
- 小クラスは親クラスの特化（specialization）であるとも言える。
- JVM は常に、ターゲットオブジェクトの実際のクラスから出発して継承階層を上方向に検索し、目的のメソッドのシグネチャにマッチする最初のものを検出する。呼び出された時点でのオブジェクトの見かけ上の型は関係ない。


## 型の安全性と定数
- オブジェクト参照への無意味な代入を防止したい場合には、メソッドのパラメータを final として宣言する
- 変更可能オブジェクトを変更不能として振る舞わせるには、読み取り専用の interface を使う
- 定数を利用する根本的な理由は、オブジェクトの状態に対する望ましくない変更を減らすこと
  - システムがより安定し、信頼性が高まる

## 例外
- Throwable
  - 実行時に発生する問題を処理するためのメカニズム
  - Error と Exception
- 可能な限り多くの例外を**明示的に** catch する。catch(Exception) を唯一の例外ハンドラとして使うことは避ける。
- 例外は設計フェーズの間に見定めておく


## コールバック
電話をかけ、責任者と話したいと言う。その時、おそらく「ただいま多忙でして...」などと返ってくる。そこで取りうる選択肢として、

- あとで改めてかけ直す
  - ポーリング
- 電話回線を繋いだまま待つ
  - 同期処理
- 自分の電話番号を伝えて切る
  - コールバック

### ポーリング
何らかの変更が生じたかどうかを調べるために、クライアントが別のオブジェクトのメソッドを繰り返し呼び出すことをいう

RDB のトリガー？

### 同期メソッド呼び出し
一旦メソッドが呼び出されると、例外が投げられるか、あるいはメソッドが正常に return するまで、呼び出し側のコードはブロックする

### コールバックの仕組み
2種類の当事者が存在する。**クライアント**とも言われる Caller（呼び出し側）と、サーバとも言われる Receiver（受け側）である。

Receiver は、適切な状況が発生した場合に Caller に対してコールバックを実行する責務を負う。一般に Receiver と Caller とは、別々のスレッドあるいはプロセスで時効される。もしそうでなければ、このコールバックというイディオムから得られるものは少ししかないだろう。

### コールバックを実装する


### マルチキャストコールバック


## クラスのロードとオブジェクト生成
- クラスの自動ロード（JVM が自動的にこっそりと行う）が行われるのは以下の２つのタイミング
  - クラスの static なメソッドあるいはフィールドがアクセスされた結果、クラスベースの情報をロードする必要が生じた場合
  - まだ参照されたことのないクラスのオブジェクトインスタンスが、キーワード new によって初めて生成された場合
- クラスがロードされた時点で、Java 実行環境は該当のクラス中で宣言されている static 初期化子を全て実行することを要求される。
- コンストラクタチェーンを利用することによって、こんすたクタの振る舞いやデフォルト値がチェーン中の１箇所だけに現れるようにする。
- 抽象クラスのコンストラクタからは、決して具象クラスのメソッド　を呼び出さない。


## 生成に関するイディオム
- オブジェクトファクトリ
- Factory メソッド
- Abstract Factory
- Singleton
- Singleton アダプタ
- 「仮想」コンストラクタ

### オブジェクトファクトリ
クライアント側のコードに対してオブジェクト生成に責任を負う工場のこと

```java
Product p = factory.makeProduct();
```

### Factory メソッド
具象型を完全に隠蔽させるには、"Factory メソッド"というイディオムを使う。

```java
interface NodeMaker {
    Node makeNode();
}

class NodeMakerImpl implements NodeMaker {
    Node makeNode() {
        return new VideoNode();
    }
}
```

このようにして、具象クラスへの参照をクライアントコードから完全に排除することが可能になる。

```java
NodeMaker noder = new NodeMakerImpl();
Nde outputNode = noder.makeNode();
outputNode.configure();
```

### Singleton
```java
public class Singleton{

    private Singleton() {}

    static private Singleton instance_ = new Singleton();

    static public Singleton instance() {
        return instance_;
    }
}
```

#### Singleton が、ガベージコレクタに回収されないようにするには！？
- -Xnoclassgc フラグで実行
  - Singleton 以外の使われていないクラスもメモリ上に残る
- システムで使われる Singleton クラス群のレジストリを保持する
  - クライアントコードのどこかで、全ての Singleton クラスのインスタンスの Vector を保持する

```java
public class Client {
    // クラスの GC を停止させるためだけに使われる Singleton レジストリ
    private Vector singletons_ = new Vector();

    public Client() {
        singletons_.addElement(Singleton.instance());
        // etc.
    }
}
```


## パフォーマンスとリソースのバランス


### 怠惰なインスタンス化
- 具象 Singleton クラスでは、怠惰なインスタンス化を避ける
- クライアントクラスによって直接あるいは間接に呼び出される可能性がある場合、怠惰なインスタンス化を使ったメソッドは「スレッドに安全」にする
- これはメモリが少ない時には、多少の効果があった（だろう）

```java
class Singleton {
    static public Singleton instance() {
        if (instance_ == null) {
            instance_ = new Singleton();
        }

        return instance_;
    }
}
```

- 怠惰なインスタンス化を使ったメソッドを保護するためにダブルチェックを使う

```java
class Singleton {
    static public Singleton instance() {
        // ブロッキングの処理は重いので、ここではブロックさせたくない
        if (instance_ == null) {
            // 複数のスレッドがここにある可能性あり
            synchronized(Singleton.class) {
                // ここで再度チェック
                if (instance_ == null) {
                    // 安全
                    instance_ = new Singleton();
                }
            }
        }

        return instance_;
    }
}
```

### 意欲的なインスタンス化
- 怠惰なインスタンス化と正反対
- メソッド`class.forName()`
- 以下の例は、String　オブジェクトの配列を受け取ってクラスを強制的にロードさせるメソッド
```java
public Class [] loadClasses(String [] classnames) throws ClassNotFoundException {
    int num = classnames.length;
    Class [] classes = new Class[num]
    for (int i = 0; i < num; i+=) {
        classes[i] = Class.forName(classnames[i]);
    }
    return classes;
}
```


## コレクション
- オブジェクトのインスタンス群を管理しやすい方法でまとめるのに使われる。
- 表面には現れないが、コレクションのインタフェースで定義されるメソッドは、さまざまなデータ構造を使って実装することができる。
  - 例えば、リンクリスト、ハッシュテーブル、２分木
- 2種類
  - 標準コレクションクラス
  - 均質コレクションクラス


## イテレータ

