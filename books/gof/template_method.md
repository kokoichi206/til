# Template Method
具体的な処理をサブクラスに任せる

## テンプレートとは何か
テンプレートというのは、文字の形に穴が空いている薄いプラスチックの板のこと。その穴をペンでなぞると、手書きでも整った文字を書くことができる。

テンプレートの穴を見ればどのような形の文字が書けるかは分かりますが、実際にどういう文字になるかは、具体的な筆記用具が決まらなければわからない。

**スーパークラスで処理の枠組みを定め、サブクラスでその具体的内容を定めるようなデザインパターン**を、

Template Method パターン

という。

```java
// AbstractDisplay.java
public abstract class AbstractDisplay {
    public abstract void open();
    public abstract void print();
    public abstract void close();
    public final void display() {
        open();
        for (int i = 0; i < 5; i++) {
            print();
        }
        close();
    }

}

// CharDisplay.java
public class CharDisplay extends AbstractDisplay {

    private char ch;
    public CharDisplay(char ch) {
        this.ch = ch;
    }
    public void open() {
        System.out.print("<<");
    }
    public void print() {
        System.out.print(ch);
    }
    public void close() {
        System.out.println(">>");
    }

}
```

## ヒント

### ロジックが共通化できる
スーパークラスのテンプレートメソッドでアルゴリズムが記述されているので、サブクラス側ではアルゴリズムをいちいち記述する必要がなくなる。

### スーパークラストサブクラスの連携プレー
スーパークラスの実装をよく理解しておく必要がある。

**スーパークラスの記述を多くすれば、サブクラスの記述は楽になるが、サブクラスの自由度は減る。**どのレベルで処理を分けるか、その辺の感覚は難しい？

### サブクラスをスーパークラスと同一視する
スーパークラス型の変数に、サブクラスのインスタンスのどれを代入しても正しく動作するようにする、という原則は The Liskov Substitution Principle（LSP）と呼ばれる。

この LSP は、Template Method パターンに限らない、継承の一般的な原則！
