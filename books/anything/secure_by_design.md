# Secure by Design

本来 30 文字までしか入力できないはずが、それを超えて入力できてしまうバグ。発見者は、「パスワードの入力フィールドに 32000 文字をこす文字列を入力すると、アプリケーションがクラッシュする」という、過度の文字数のデータを入力することでアプリケーション・サーバをクラッシュさせる DoS(Denial-of-Service)攻撃につながる脆弱性として報告してきた。

julie undefined という名前で登録を行い、システムをクラッシュさせた！

いくら金庫室に強力な錠前と重いドアを備えたとしても、そのドアのちょうつがいを壊してドアを外してしまえば、錠前や重いドアの意味がなくなってしまう。

結局のところ、絶対的な意味において安全なシシテムなど存在しない。**設計においてまず第一に考えないといけないことはセキュリティである**！セキュリティは最後に付け足せるものではなく、開発者がどれほど強い意志を持っていたとしても、それを成し遂げることは簡単ではない。

セキュリティは開発者が選択したデータの型の中にあり、そのデータの型をどのようにコードで表現するのかにかかっている。同様に、セキュリティは開発時に使われるドメイン言語の中にあり、ドメインの概念やビジネスルールをいかに忠実にモデリングしているかにかかっている。そして、セキュリティはビジネスドメインとそのドメインに属する顧客の要望に応えるために開発したツールとの間にある認識の差を減らすことで得られるものである！

Behavior-Driven Development: を取り入れた場合、テストメソッドの名前は長くなる傾向がある。BDDでは、開発者ではない人にもなんのテストなのかを理解させる目的がある。


## sec 1
- セキュリティを機能（feature）ではなく心配事（concern）として見ること
- 設計とは何か？なぜセキュリティにとって重要か
- 良い設計がセキュリティの強化につながること
- Billion Laughs 攻撃への対策
    - XMLパーサを対象としたDoS攻撃
    - lol が使われることが多いため

### セキュリティを機能ではなく心配事として捉えること
機能をつけたとしても、心配事が解決できるわけではない！

### セキュリティの機能と心配事
ユーザストーリ（「○○のユーザとして、私は△△の機能が欲しいです。そうすることで、□□を達成することができるようになります。」）がしばしば使われる。このように、ソフトウェアの開発では、機能に焦点が当てられているため、セキュリティについて説明する際、同じように機能について述べられていても不思議ではない。

「ログイン機能を実施」という機能にフォーカスしていたのでは、ログインしてないけど URL を知っている人がアクセスできる状況など、への考慮が漏れる可能性？

セキュリティを機能として持つことではなく、セキュリティに関する心配事、外部に秘密にすべき情報が漏れないようにする**機密性(confidentiality)**、を解決すること！

### セキュリティにおける心配事の分類：CIA-T
- 機密性：Confidentiality
    - 外部に知られるべきでない情報を絶対に漏れないようにする
    - 医療記録
- 完全生：Integrity
    - 情報が変更されないこと
    - 選挙における投票数の集計
- 可用性：Availability
    - 取得可能なデータを必要な時に取得できること
    - 消防隊員が火事の場所を知ることができる
- Traceability：追跡可能性
    - 誰がどのデータにいつアクセス・変更したかを把握できること

セキュリティに関する心配ごとは尽きることがなく、全ての時間を使う必要が出てくる。

⇨ セキュリティを開発者の作業やソフトウェアの設計に組み込む！

### 設計（design）とは何か
一般的に「設計」という言葉はあまり深く考えずに使われている。

もし、１０人の開発者に対して「ソフトウェア開発においてどのような行為が設計とみなされるのか？」を尋ねたら、それぞれ異なる答えが返ってくるだろう。（多くの人は、ドメイン・モデルの抽出、API設計、デザイン・パターンの適応、システムのアーキテクチャ、などを応える亜浪）

本書での答えは、ソフトウェア開発で行われる全ての行為が設計の行為であり、これら全ての行為が設計プロセスの一部として扱われるべき（if文、ハッシュテーブル等）。システムやソフトウェアは実装されてプロダクトとしてリリースされるまで、安定した設計の状態であるとは言えない。

つまり、能動的な意思決定が求められる行為は。全て設計プロセスの一部とみなされる！

### セキュリティにおける従来のアプローチとその欠点
セキュリティの優先度を最も高くするため、開発者自身がトレーニングを受けたり、その経験をしておく必要がある。一般的にこのアプローチの場合、開発者が守らなければならない特定のタスクやアクションが課せられることとなる。

XSS(Cross-Site-Scripting)

`<script>alert(42);</script>`など

``` java
public class User {

    private final Long id;
    private final String usename;

    public User(final Long id, final String username) {
        notNull(id);
        notNull(username);

        this.id = id;
        this.username = validateForXSS(username);
    }
}
```

実際に上記のように妥当性確認の質を上げることはよくあるが、次のような理由で問題が発生する

- 開発者はビジネスロジックをどのように実装するのかを考慮しつつ、セキュリティの脆弱性についても考えなくてはならない
- 全ての開発者に対してセキュリティの専門家と同じレベルのセキュリティに関する知識が求められる
- 実装を行う開発者は今後起こり得る全ての脆弱性を把握していることが前提となる

### 設計による安全性の向上
作成するソフトウェアに対して可能な限り最高の水準を維持する設計を常に心がける。意識する対象を設計に移すことで、セキュリティを常に意識し続ける必要はなくなり、ソフトウェアの安全性を高い水準で確立できるようになる。

### セキュアバイデザインの適応
まず、このアプリケーションのコンテキストにおいて、ユーザ名が意味するところをドメイン・エキスパートと共に見つけ出す。

``` java
public class User {

    private static final int USERNAME_MINIMUM_LENGTH = 4;
    private static final int USERNAME_MAXIMUM_LENGTH = 40;
    private static final String USERNAME_VALID_CHARACTERS = "[A-Za-z0-9_-]"+;

    private final Long id;
    private final String username;

    public User(final Long id, final String username) {
        notNull(id);
        notNull(username);

        final String trimmed = usename.trim();
        inclusiveBetween(USERNAME_MINIMUM_LENGTH,
                        USERNAME_MAXIMUM_LENGTH,
                        trimmed.length());
        matchesPattern(trimmed,
                    USERNAME_VALID_CHARACTERS,
                    "Allowed characters are: %s",
                    USERNAME_VALID_CHARACTERS);
        
        this.id = id;
        this.username = trimmed;
    }
}
```

ユーザ名をドメイン・モデルの中に明示的に抽出を行うことで、ユーザ名が重要な概念のように思えることに加え、ユーザ名の妥当性確認に関するロジックを１つのクラスにまとめることで高凝集の原則に従うことにもなる！

ユーザ名を表す Username クラスを作成し、ユーザ名に関するロジックをこの Username クラスに移動させる。こうすることで、ユーザ名に関する全ての知識がこのクラスの中でカプセル化される。

**ドメイン・プリミティブ（domain primitive）**

``` java
public class Username {

    // Username クラスに切り出したことで、
    // Username の情報であることは明らかなので、
    // USERNAME_ は記述しない！
    private static final int MINIMUM_LENGTH = 4;
    private static final int MAXIMUM_LENGTH = 40;
    private static final String VALID_CHARACTERS = "[A-Za-z0-9_-]"+;

    private final String value;

    private final Long id;
    private final String username;

    public User(final String value) {
        notBlank(value);

        final String trimmed = usename.trim();
        inclusiveBetween(MINIMUM_LENGTH,
                        MAXIMUM_LENGTH,
                        trimmed.length());
        matchesPattern(trimmed,
                    VALID_CHARACTERS,
                    "Allowed characters are: %s",
                    VALID_CHARACTERS);
        
        this.value = trimmed;
    }
}
```

``` java
public class User {

    private final Long id;
    private final String username; // 常に正しい値であることが保証される

    public User(final Long id, final Username username) {
        this.id = notNull(id);
        this.username = notNull(username);
    }
}
```

### 設計を意識するアプローチによるメリット
- ソフトウェアの設計はほとんどの開発者にとっての興味の中心であり、開発者が最も得意とするものであるため、開発者はセキュアバイデザインのコンセプトを簡単に取り入れるから
- 設計を中心に考えることで、ビジネスおよびセキュリティに関する心配事がドメインエキスパートと開発者の両者にとって同等の優先度を持つようになるから
- 優れた設計のパターンを衣取り入れることで、セキュリティの専門家でなくても安全なコードを書けるようになるから
    - また、設計を中心に考えることで、セキュリティに関して専門家だけではなく、全てのステークホルダーが議論に参加できるようになる！
- ドメインを意識することで、気がつかないうちにセキュリティに関する多くのバグを取り除けるようになるから

ユーザ名は制約のないランダムな文字の集まりではなく、そのドメインにおいて正確な意味と目的をもって定義されている概念、ということを表すために Username クラスを定義したり。

### 文字列、XML、そしてBillion Laughs 攻撃への対応
データを文字列などの汎用的なクラスで受取、**名前による指定**で行う傾向が多い。が、これをやめ、Username クラスなどの、制約を持った厳格なドメインの型を使う・

#### 妥当性確認(validation)は、次の順番で実施する
1. サイズの確認
    * 入力値の文字数は想定している範囲内に収まっているか
2. 字句的内容（lexical content）の確認
    * 入力値には正当な文字および正しいエンコードが使われているか
    * xml の構造等
        * SAX (Simple API for XML)
3. 構文（syntax）の確認
    * 入力値は正しいフォーマットに従っているか

#### XML
XML で実行可能なさまざまな機能が存在する。

#### XML のエンティティ
名前をつけることで指定した値を参照できるようにする強力な構造体のこと。

``` xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE example [
    <!ELEMENT example (#PCDATA)>
    <!ENTITY title "Secure by Design">
]>
<!-- 名前が「title」のエンティティ -->
<example>&title;</example>
```

エンティティを使って値を参照する機能は便利だが、攻撃の手段になってしまうことがある。

#### Billion laughs 攻撃
シンプルでありながらもシステムに大きな影響を与える攻撃。この核となっているのは、エンティティがXMLパーサによって値に置き換えられるという性質の悪用。

``` xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE example [
    <!ELEMENT lolz (#PCDATA)>
    <!ENTITY lol "lol">
    <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
    <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
    ...
    <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<!-- エンティティが繰り返し展開される -->
<lolz>&lol9;</lolz>
```

#### XMLパーサの設定
全てのXMLパーサが同じ挙動をするわけではないので、この対応は意外と難しい。

セキュリティの心配事とビジネスの必要性を比べる。

``` java
// OWSASP が推奨する XML パーサの設定

import static javax.xml.XMLConstants.FEATURE_SECURE_PROCESSING;

public final class XMLParser {
    static final String DISALLOW_DOCTYPE =
         "http://apache.org/xml/features/disallow-doctype-decl";
     static final String ALLOW_EXT_GEN_ENTITIES =
         "http://xml.org/sax/features/external-general-entities";
    static final String ALLOW_EXT_PARAM_ENTITIES =
         "http://xml.org/sax/features/external-parameter-entities";
    static final String ALLOW_EXTERNAL_DTD =
         "http://apache.org/xml/features/nonvalidating/load-external-dtd";

    public static Document parse(final InputStream input)
            throws SAXException, IOException {
        try {
            final DocumentBuilderFactory factory =
                                DocumentBuilderFactory.newInstance();

            factory.setExpandEntityReferences(false);       
            factory.setFeature(FEATURE_SECURE_PROCESSING,       
                                                    true);
            factory.setFeature(DISALLOW_DOCTYPE, true);     
            factory.setFeature(ALLOW_EXT_GEN_ENTITIES,          
                                                false);
            factory.setFeature(ALLOW_EXT_PARAM_ENTITIES,    
                                                false);
            factory.setFeature(ALLOW_EXTERNAL_DTD, false);      

            return factory.newDocumentBuilder().parse(input);
        } catch(ParserConfigurationException e) {
            throw new IllegalStateException("Configuration Error", e);
        }
    }
}
```

例えこのパーサーを推奨されたものにしても、もしかしたら、別のリスクに晒されているかもしれない。このような懸念は当然のことであり、このことに対応するために本書が推奨するのは、セキュリティの層をもう１つ追加すること。その層とは**設計: design**のこと

#### 設計を中心とした考え方の適応
XMLの構造的な問題として扱うのではなく、そのXMLを受け取るシステム側の妥当性確認(validation)の問題として捉えるべき。言い換えると、XMLを受け取るシステムは悪意のあるXMLのブロックをXMlパーサに解析させることなく拒否しなければならない！！！

SAP などを使って、**字句的内容**をチェックする（要素の出現回数、Billion Laughs も？）。XMLの意味に関する分析は含めない。含めてしまうと、それは結局、XMLパーサの処理をさせているのと同じことになってしまい、問題が発生する。

システム間でデータをやり取りする場合、データを受け取る側は自由度を高くし、データを送信する側はプロトコルに厳密に従うことが良いとされている。

#### XML を処理する上での制約の適用
エンティティが展開される、その性質自体がエンティティを危険なものにしているわけではない。そうではなく、結果として消費されるメモリーの量が問題。

パーサの処理に関して何らかの制約(メモリーの制限や上限など)を加える、などが考えられる。

多数のパーサが同時に走った時の解析なども考える必要があり、XMLの解析を他のプロセスとは切り離して行うなどの設計が必要となる。


#### 多層セキュリティ
ほとんどの開発現場では、Billion Laughs 攻撃に対して、XMLパーサの設定を行なっただけで対策を終わりにしてしまう傾向がある。これだけだと、家の周りをフェンスで囲んで侵入されることを防いでいるにもかかわらず、家の鍵をかけていないのと同じようなもの・

最終的には、OWASPが推奨するXMLパーサの設定、字句的内容の確認、処理場の制約を全て組み込むことで、Billion Laughs 攻撃などの攻撃をすることが非常に難しくなる。これが、まさに、セキュアバイデザインが意味するところ。つまり、設計を安全なソフトウェアを作成するための第一のツールとして利用し、設計を意識することで、作成するソフトウェアの安全性を高められるようにする。


## sec 2
- 浅いモデリング（shallow modeling）による弊害
- 深いモデリング（deep modeling）とは何か
- ビジネス的観点における完全生（integrity）の破綻によって生じるセキュリティの欠陥
- 深いモデリングによるリスクの軽減 

### ビジネスルールの観点における完全性（integrity）の問題
オンライン書籍にて「-1」冊の本を注文できてしまう。そしてその注文によって、返金を行うシステムになってしまっていた。

対象となるデータは許可されていない方法では変更や生成ができない、という完全性が保証されていない。

### 浅いモデリング
問題が生まれるのはモデリングが原因であることが多く、開発者がうまくモデリングできたと最初に思った時点で、それ以上は深く考えたり疑問んを医大狩りすることをやめてしまい、さらにそれ以降の計画を立てたり考慮したりすることをやめてしまったからだと考えている。このようなその場しのぎのモデリングのことを、浅いモデリングと呼んでいる。

今回は、冊数にマイナスを認めたのが間違いだったことは明らかであるが、なぜこのような設計になったのか。内部で管理する分には、返品対応や棚卸しでの調整など、マイナスの冊数を含めておいた方がいいこともある（多く振込すぎたなど）。

> 金額に関する概念を float で表現することは決してしたらだめ！(see sec 12)

ビジネスにおいて意味のある概念が、int, float, double, String, boolean などの基本データ型で表現されてしまう。しかし、概念に対してこのような暗黙的な表現がされてしまうことは珍しいことではない。残念なことに、このような表現はさまざまな問題を引き起こす原因となってしまう。

概念を基本データ型で暗黙的に表現してしまうと、その結果、コードも非常にわかりづらいものになってしまう。

### 深いモデリング
コードとは**コード化された知識**のことであり、まさに名前がそのことを表現する！！


#### 暗黙的な表現から明示的な表現への変換
全ての概念を明示的に表現することへの反対意見としてよく聞くのが、クラスの数があまりにも多くなる、というもの。しかし、概念を表現するクラスに記述されるコードは全て必要なものである！！

そのため、重要なビジネスルールは全てコード上に表現されることになり、仮に、それができていなければ、構築されるシステムの質が落ちることとなる。

> モデリングを行う際は、暗黙的に表現された概念を明示的に表現するように変えていく！

また、浅いモデリングを行うと、対象のドメインについて理解する機会を失うことにもなる。そうなってしまうと、ここまで見たように、セキュリティの問題となる原因を抱え込む可能性も高くなる。



















## メモ

### 開発一般原則
- 高凝集：high cohesion
- 疎結合：low coupling
- インターフェースの利用
- 依存性逆転の原則：Dependency Inversion Principle (DIP)
- 不変性：immutability

### memo
- システム間でデータをやり取りする場合、データを受け取る側は自由度を高くし、データを送信する側はプロトコルに厳密に従うことが良いとされている。
    - [寛容な読み手パターン](https://martinfowler.com/bliki/TolerantReader.html)
- 金額に関する概念を float で表現することは決してしたらだめ！(see sec 12)
- ドメイン・プリミティブ

### Links
- [OWASP Top 10](https://owasp.org/Top10/ja/)

### 疑問
- sec1, XML パーサのところの話
    - XML パーサなどの脆弱性への知識がないと、結局対策できなくない？

