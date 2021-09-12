# Chain of Responsibility
責任のたらい回し

## Chain of Responsibility パターン

### Trouble クラス
```java
public class Trouble {
    private int number;
    public Trouble(int number) {
        this.number = number;
    }
    public int getNumber() {
        return number;
    }
    public String toString() {
        return "[Trouble ]" + number + "]";
    }
}
```

### Support クラス
トラブルを解決する連鎖を作るための抽象クラス。

next フィールドは、たらい回しする先を指定する。setNext メソッドはたらい回しする先を設定する。

```java
public abstract class Support {
    private String name;
    private Support next;
    public Support(String name) {
        this.name = name;
    }
    public Support setNext(Support next) {
        this.next = next;
        return next;
    }
    public final void support(Trouble trouble) {
        if (resolve(trouble)) {
            done(trouble);
        } else if (next != null) {
            next.support(trouble);
        } else {
            fail(trouble);
        }
    }
    public String toString() {
        return "[" + name + "]";
    }
    protected abstract boolean resolve(Trouble trouble);
    protected void done(Trouble trouble) {
        System.out.println(trouble + " is resolved by " + this + ".");
    }
    protected void fail(Trouble trouble) {
        System.out.println(trouble + " is cannot be resolved");
    }
}
```

### NoSupport クラス
Support クラスのサブクラス。resolve メソッドが常に false を返すもの。すなわち、「自分は何も問題を処理しなというクラス」

```java
public class NoSupport extends Support {
    public NoSupport(String name) {
        super(name);
    }
    protected boolean resolve(Trouble trouble) {
        return false;
    }
}
```

### LimitSupport クラス
limit dえ指定した番号未満のトラブルを解決するクラスを作る

```java
public class LimitSupport extends Support {
    private int limit;
    public LimitSupport(String name, int limit) {
        super(name);
        this.limit = limit;
    }
    protected boolean resolve(Trouble trouble) {
        if (trouble.getNumber() < limit) {
            return true;
        } else {
            return false;
        }
    }
}
```

### OddSupport クラス
```java
public class OddSupport extends Support {
    public OddSupport(String name) {
        super(name);
    }
    protected boolean resolve(Trouble trouble) {
        if (trouble.getNumber() % 2 == 1) {
            return true;
        } else {
            return false;
        }
    }
}
```

### Main クラス
```java
public class Main {
    public static void main(String[] args) {
        Support alice = new NoSupport("Alice");
        Support bob = new LimitSupport("Bob", 100);
        Support elmo = new OddSupport("Elmo");
        Support fred = new LimitSupport("Fred", 300);
        // 連鎖の形成
        alice.setNext(bob).setNext(elmo).setNext(fred);
    }
    // さまざまなトラブル発生
    for (int i = 0; i < 500; i += 33) {
        alice.support(new Trouble(i));
    }
}
```

## ヒント

### 要求を出す人と要求を処理する人を緩やかに結びつける
Chain of Responsibility パターンのポイントは、要求を出す人と要求を処理する人を緩やかに結びつけるところ。

**もしこのパターンを使わないと、「この要求はこの人が処理すべし」という知識を誰かが中央集権的に持っている必要がある。**その知識を「要求を出す人」に持たせるのはあんまり賢明ではない。部品としての独立性が損なわれてしまうから。

### 同的に連鎖の形態を変える
ウインドウシステムでは、ユーザがウインドウ状にコンポーネントを自由に追加できる場合がある。このようなときには Chain of Responsibility パターンが有効に働く。

### 注意点
確かに、中央集権的な管理と比べると、処理は遅くなる
