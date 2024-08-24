## なんでも

- [Astro](https://github.com/withastro/astro)
  - content driven web framework
  - high performance
  - ほかのフレームワークを統合して使うことも可能！！
    - **React, Vue, Svelte,.. などと同時に使用できる！**
  - why 高速
    - **アラインドアーキテクチャ**
    - 静的なコンテンツと動的なコンテンツに分ける
  - Astro DB
    - 静的なサイトでのユーザー認証、フォームによるコメント投稿など
- DNS
  - 失効ドメインを狙う
    - ドロップキャッチ
    - バックオーダリング
  - Wi-Fi ルータ欲しい
- Ubuntu
  - 両立している
    - コミュニティによるオープンな開発
    - 企業によるエンタープライズレベルのサポート
  - **タイムベースリリース**
    - 半年に一度リリース
    - 24.04 -> 2024 年の 4 月にリリース
    - 通常は9ヶ月のサポート期間
  - LTS 版
    - 偶数年の4月
    - 5年のサポートが約束されている
  - 提供の形態
    - Ubuntu Desktop
    - Ubuntu Server
    - Ubuntu Core
      - IoT
    - コンテナイメージ
    - クラウド
    - WSL
  - LXD
    - Kubernetes ほど大規模でなく Docker ほどイミュータブルではない隔離環境！
  - GNOME
    - デスクトップ環境の1つ
      - 統一感を出すため
- zozo
  - ADR
    - タイトル
    - コンテキスト
    - 決定
    - ステータス
    - 結果
  - 書きたいかも
    - issue に書いておくのとどう違う？
    - より見つけやすい
- **Chrome V8**
  - JavaScript エンジン
    - JavaScript の処理系
    - v8 自体は + して webassembly の仕様も実差王sれている
  - [v8](https://github.com/v8/v8)
    - パフォーマンスを改良したもの
  - **v8 の特徴**
    - 動的マシンコード生成: JIT コンパイラ
      - 中間表現・バイトコードを全く使わない、
      - CPU が直接実行できるマシンコードへコンパイルする！
    - Hidden Class + インラインキャッシュ
      - Hidden Class
        - メモリのオフセット位置を持つことで高速に
    - ガベージコレクション
      - **正確な** GC
- RDBMS
  - パーティショニング
    - データが特定のルールで増えていくことがわかっている場合に有効
  - シャーディング
  - 書き込みを非同期に行う
- Cloudflare Workers
  - CDN
    - コンテンツ配信周りを強化して、地理的に分散させたリバースプロキシ
  - エッジ
    - CDN ににた機能を持ちつつも、
    - 足りない機能を自由に実装できる、サーバーレス実行基盤
    - FaaS の側面
      - 実行単位を跨いでメモリを共有できない
  - キャッシュのさせかた
    - 拡張された fetch
      - Web 標準から一部拡張している
    - Cache API
  - キャッシュの状態
    - fresh
    - stable
      - stable を一旦返しつつ、新しい情報を裏で取得する、などもできるらしい
  - ディレクティブ
    - `no-cache`
      - キャッシュが stable かどうかに関わらず、必ずキャッシュの revalidate を要求するもの！
    - `no-store`
      - キャッシュしない
  - Cloudflare Workers
    - shared cache
    - FaaS 基盤
- AWS
  - Lightsail
    - Lightsail for Research とかもあるらしい
  - サーバーレスで静的 Web サイトを配信もできるらしい！！

## TypeScript

- TypeScript
  - 大規模開発を目的とした、静的型付けの機能
  - AltJS の一種
    - JavaScript にコンパイルされる
- 型注釈を書いたほうがいい
- AltJS
  - TypeScript
    - **JavaScript からの移行ハードルの低さがある！**
- **TypeScript は JavaScript のスーパーセット**
  - **すべての JavaScript のプログラムは、文法的に有効な TypeScript のプログラムでもある！**
- any による型検査のスキップ！
  - 型検査器
    - 型と操作
- **Union 型**
- 部分型関係
  - AdminUser のインスタンスを User インスタンスとして扱っても安全である、など
  - ポリモーフィズム的なやつ
- **型システムには名前的なものと構造的なものがある**
  - TypeScript の部分型関係は構造的らしい
    - Java では `{ id: string }` のように、名前のない型はかけない

``` typescript
const middleName: string | null = prompt(
    "pi:"
);
console.log(middleName);
console.log(typeof middleName)
if (middleName !== null) {
    console.log(middleName.length)
}

const adminUser: { id: string; permission: string } = {
    id: " pipipi",
    permission: "admin",
}
const user: { id: string } = adminUser;
console.log("user.id: " + user.id);
```

- JavaScript の全ての式 (Expression) は TypeScript の型で表現可能
- プリミティブ
- オブジェクト
  - オブジェクト
  - 配列
  - 関数
  - 正規表現
  - Promise
  - Date
  - ほか多数
- 型エイリアス
- **型推論**: type inference
  - 文字列のリテラル型、とか
  - widening: 型の拡大
    - プロパティがより広い型に拡大されること
  - オブジェクトのプロパティは書き換えが可能
- **const が制限できるのはオブジェクトの『再代入』**
  - **`as const` でオブジェクトのプロパティをリテラル型に推論する！**
    - **全てのプロパティが読み取り専用となる**
- リテラル型
  - **プリミティブ型をさらに細分化して、特定の値のみを受け入れる型のこと**
  - **リテラル型 ✖️ Union めっちゃいい**
- Union 型
  - enum は昔からある機能だけど、あんまり使われていない
  - Union に対する専用の絞り込み
    - **flow-sensitive typing**
- never 型
  - ありえない、ことを示す型
- **タグ付き Union**
  - **ただのオブジェクト同士の Union 型でうまく絞り込みをするためのテクニック**
- **ないかもしれない**
  - null, undefined
    - どちらを使うかは、状況や好みによる
- **成功と失敗の表現**
  - **ジェネリック型**
    - 型引数を持つ型
- **型に最大限の情報を込める**
  - ふるい型、依存型、などもある言語もある

``` typescript
// タプル型の例
const dataList1: [string, string, number] = ["hi", "pi", 23]

// あれ、これが型エイリアスらしい
type User = {
    name: string;
    age: number;
};

const user: User = {
    name: "ww",
    age: 150,
};
user.name = "aree";
user.age = 100;

const date: Date = new Date();
console.log(date);

const myName: "鈴木" = "鈴木";

const userAsConst = {
    name: "osshoi",
    age: 130,
} as const satisfies User;
// readonly になるので string とかになる必要はなく、より詳しいリテラル型に推論される。
// Cannot assign to 'name' because it is a read-only property.(2540)
// userAsConst.name = "aree";
// userAsConst.age = 100;

// コレと satisfies って変わりある？
// const userAsConst2: User = {
//     name: "osshoi",
//     age: 130,
// } as const;


type MarkerPosition = "start" | "end";
function placeMarker(position: MarkerPosition): void {
    switch (position) {
        case "start":
            console.log(position);
            break;
        case "end":
            console.log(position);
            break;
        // switch が Union 型を網羅してなくてもコンパイルが通ってしまう。
        default:
            // Type 'string' is not assignable to type 'never'.(2322)
            // const _: never = position;
            position satisfies never;
    }
}
placeMarker("end")
placeMarker("start")


// タグ付き Union
type Circle = { type: "circle"; radius: number };
type Rectangle = { type: "rectangle"; width: number; height: number };
type Shape = Circle | Rectangle;
const getArea = (shape: Shape): number => {
    switch (shape.type) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "rectangle":
            return shape.width * shape.height;
        // この関数では網羅性のチェックは不要！
        // return で number を返す必要がある関数のため
    }
}


type Options1 = {
    encoding?: string;
};
type Options2 = {
    encoding: string | undefined;
};
// ライブラリとして公開する場合は利便性を重視してこっちを使うことが多いかも。
const o1: Options1 = {};
// 省略はできないので、こっちの方がいい！
const o2: Options2 = { encoding: undefined, };


type Success<T> = { success: true; value: T };
type Failure<E> = { success: false; error: E };
// type Result<T, E = unknown> = Success<T> | Failure<E>;
type Result<T, E> = Success<T> | Failure<E>;
function readData(): Result<string, Error> {
    if (Math.random() < 0.5) {
        return { success: true, value: "data" };
    } else {
        return { success: false, error: new Error("failed to read data") };
    }
}
const result = readData();
if (result.success) {
    console.log(result.value);
} else {
    console.log(result.error);
}
```

- 型の関係性
  - 名前的型付け
  - 構造的型付け
    - **Go, TypeScript**
    - Go は部分的な気がする
- 型と型の関係性を階層構造としてみた時
  - 上位を基本型 (supertype)
    - 抽象的な型
  - 下位を部分型 (subtype)
- 名前的型付け
  - **名前的部分型**: nominal subtype
    - extends とか
- 構造的型付け
  - **構造的部分型**: structural subtype
- **ダックタイピング**
  - JSON.stringify
- TypeScript
  - **JavaScript との互換性を考慮した結果、構造的型付けになっている**
    - ダックタイピング
    - オブジェクトリテラル
      - その場でオブジェクトを生成する
  - 意図せずに互換性が生じる点は注意
- **TypeScript で名前的型付けを実現する**
  - private プロパティを持つクラス
  - ブランド型: Branded Type
    - 型を区別するためのプロパティを型に持たせる

``` typescript
type Hoge = {
    id: number;
    name: string;
};
type PPP = {
    id: number;
}
const h: Hoge = { id: 3, name: "p" };
const p: PPP = h;

class Shape {
    area(): number {
        return 0;
    }
}
class Circle {
    radius: number;

    constructor(radius: number) {
        this.radius = radius;
    }

    area(): number {
        return Math.PI * this.radius ** 2;
    }
}
const shape: Shape = new Circle(1);
console.log(shape.area())

JSON.stringify(shape)


interface UserId {
    __brand: "UserId"
    id: number;
}
const userId = { id: 1 } as UserId;
```

- 関数のような型が定義できたりする
  - 入力された型に対して別の型を返す
- へー, infer とかあるんか
- Mapped Types
  - **in 演算子で Union 型のキーを展開する仕組み**
- never
  - extends と組み合わせて否定のパターンを作るのに便利
- **型の表現とランタイム上の値チェックは独立した概念！**

``` typescript
type T1 = {
    a: number;
    b: string;
    c: boolean;
}
type T2 = Pick<T1, "a" | "c">;
type T3 = Pick<T1, never>;

type Eq<X, Y> =
    (<T>() => T extends X ? 1 : 2) extends
    (<T>() => T extends Y ? 1 : 2) ? true : false;
type Assert<A extends true> = A;

type _0 = Assert<Eq<1, 1>>;
type _1 = [
    Assert<Eq<true, true>>,
    // @ts-expect-error
    Assert<Eq<true, false>>,
];

type T = {
    a: number;
    b: string;
};
type _ = [
    Assert<Eq<T["a"], number>>,
    Assert<Eq<T["a" | "b"], number | string>>,
];

// サブタイプ関係による型レベルの分岐表現！
// A extends B ? C : D
type R1 = true extends true ? 1 : 2; // リテラルとしての true
// type R1 = true extends boolean ? 1 : 2;
// 入力された型に対して別の型を返す関数のような型
type F<T> = T extends { v: boolean } ? 1 : 2;
type r1 = F<{v: true}>; //=> 1
type r2 = F<{v: "true"}>; //=> 2


type ValueType<T> = T extends { value: infer U } ? U : never;

// オブジェクト型から、そのキー一覧を Union 型として取り出す！
type K = keyof T;
type _k = Assert<Eq<K, "a" | "b">>;

type M = {
    // 型レベルのイテレータ的なもの、と思ってもいいかも。
    [k in keyof T]: T[k]
};
// same types
type _3 = Assert<Eq<M, { a: number; b: string; }>>;

type Pick2<T, K extends keyof T> = {
    [P in K]: T[P];
}
type _4 = [
    Assert<Eq<Pick<{ a: number; b: string }, "b">, { b: string }>>,
    Assert<Eq<Pick2<{ a: number; b: string }, "b">, { b: string }>>,
    Assert<Eq<Pick2<{ a: number; b: string }, never>, { }>>,
]


type User = {
    id: string;
    name: string;
    createdAt: number;
};
// type DraftUser = {
//     id?: string;
//     name: string;
//     createdAt?: number;
// }
type Optional<T extends {}, K extends keyof T> = Omit<T, K> & {
    [k in K]?: T[k] | undefined;
};
type DraftUser = Optional<User, "id" | "createdAt">
const _why_string: DraftUser = { name: "a2", id: "32" };

// declare async function createUser(user: DraftUser): Promise<User>;
declare function createUser(user: DraftUser): User;
const user0: User = createUser({ name: "a" });
const user1: User = createUser({ name: "b", createdAt: Date.now() });

// 一旦オブジェクトの Mapped Types として取り出すことで
type Identify<T> = T extends infer U ? { [K in keyof U]: K } : never;
// なんで infer U 入れてるんだっけ？基本 never には落ちなさそう？
// type Identify<T> = { [K in keyof T]: K };
type DraftUser2 = Identify<Optional<User, "id" | "createdAt">>
```
