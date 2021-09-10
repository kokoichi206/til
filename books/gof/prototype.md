# Prototype
コピーしてインスタンスを作る

## Prototype パターン
`new Something()`としてクラスのインスタンスを作るのではなく、クラス名を指定せずにインスタンスを生成したくなるときもある。クラスからインスタンスを作るのではなく、インスタンスをコピー（複製）して新しいインスタンスを作る。それは以下のような場合である。

1. 種類が多くてクラスにまとめられない場合
2. クラスからのインスタンス生成が難しい場合
3. フレームワークと生成するインスタンスを分けたい場合

このような場合に、**インスタンスから別のインスタンスを作り出す、Prototype パターン**という。

Java 言語では、複製を作る操作を「clone」と呼ぶ。


### Product インタフェース
Product インタフェースは、複製を可能にするためのもの。このインタフェースは、java.lang.Cloneable インタフェースを継承している。

```java
package framework;

public interface Product extends Cloneable {
    public abstract void use(String s);
    public abstract Product createClone();
}
```

### Manager クラス
Manager クラスは、Product インタフェースを利用してインスタンスの複製を行うクラス。

showcase フィールドは、インスタンスの「名前」と「インスタンス」の対応関係を、java.util.Hashtable として表現したもの。

下のコードの中に、具体クラスが含まれないことに注意。

```java
package framework;
import java.util.*;

public class Manager {
    private Hashtable showcase = new Hashtable();
    public void register(String name, Product proto) {
        showcase.put(name, proto);
    }
    public Product create(String protoname) {
        Product p = (Product)showcase.get(protoname);
        return p.createClone();
    }
}
```

### MessageBox クラス
clone でコピーを行うことができるのは、java.lang.Cloneable インタフェースを拡張したものだけ。try, catch してあげる必要がある。

```java
import framework.*;

public class MessageBox implements Product {
    private char decochar;
    public MessageBox(char decochar) {
        this.decochar = decochar;
    }
    public void use(String s) {
        int length = s.getBytes().length;
        for (int i = 0; i < length + 4; i++) {
            System.out.print(decochar);
        }
        System.out.println("");
        System.out.println(decochar + " "  + s + " " + decochar);
        for (int i = 0; i < length + 4; i++) {
            System.out.print(decochar);
        }
        System.out.println("");
    }
    public Product createClone() {
        Product p = null;
        try {
            p = (Product)clone();
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }
        return p;
    }
}
```

### Main クラス
まず Manager のインスタンスを作る。そして、Manager のインスタンスに対して、UnderlinePen のインスタンスと MessageBox のインスタンスを（名前付きで）登録する

```java
import framework.*;

public class Main {
    public static void main(String[] args) {
        Manager manager = new Manager();
        UnderlinePen upen = new UnderlinePen('~');
        MessageBox mbox = new MessageBox('*');
        MessageBox sbox = new MessageBox('/');
        manager.register("strong message", upen);
        manager.register("warning box", mbox);
        manager.register("slash box", sbox);

        Product p1 = manager.create("strong message");
        p1.use("Hello, world.");
        Product p2 = manager.create("warning box");
        p2.use("Hello, world.");
        Product p3 = manager.create("slash box");
        p3.use("Hello, world.");
    }
}
```
