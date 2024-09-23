fn addOne(i : Int) -> Int {
  i + 1
}

enum MuEnum {
  A
  B
  C
}

fn hello(self : MuEnum) -> String {
  match self {
    A => "A"
    B => "B"
    C => "C"
  }
}

enum AstNode {
  Str(String)
  Number(Double)
  // 名前付き型データ構造
  X(~Y : Int, ~Z : Int)
  Null
}

struct Point {
  x : Int
  y : Int
} derive(Show)
// } derive(Show, Eq)

fn lge[X : Compare](a : X, b : X) -> Int {
  if a < b {
    -1
  } else if a > b {
    1
  } else {
    0
  }
}

impl Compare for Point with compare(a : Point, b : Point) -> Int {
  a.x + a.y - (b.x + b.y)
}

// derive Eq もあるらすい。
impl Eq for Point with op_equal(a : Point, b : Point) -> Bool {
  a.x == b.x && a.y == b.y
}

fn distance(self : Point, other : Point) -> Double {
  let x = self.x - other.x
  let y = self.y - other.y
  (x * x + y * y).to_double().sqrt()
}

struct Point3D[T] {
  x : T
} derive(Show)

// type! は error 型の宣言
type! MyErr String derive(Show)

fn f() -> Unit!MyErr {
  raise MyErr("error dayo")
}

fn www() -> Unit! {
  // f! !!
  f!()
}

fn _s() -> Unit {
  let _ : Point3D[Int] = { x: 1 }
  let p = Point::{ x: 1, y: 2 }

}

fn yeeee() -> Unit {

}

fn main {
  println(@lib.hello())
  let world = "wwww"
  println("Yeeeaaahh, \{world}!!!")

  // mutable
  let mut y : Int = 3
  y = 3
  println("y, \{y}!!!")
  // いろんなメソッドが生えてるが WebAssembly のターゲットそのもの。
  // y.

  // map
  let map : Map[String, Int] = { "a": 1, "b": 2, "c": 3 }
  let a = map.get("a")
  println("a, \{a}!!!")
  let contains_a = map.contains("a")
  // derive(Show) で string 出力ができるようになる。
  println("contains_a, \{contains_a}!!!")

  // impl in map
  //
  //   match self.entries[idx] {
  //   Some(entry) => {
  //     if entry.hash == hash && entry.key == key {
  //       break Some(entry.value)
  //     }
  //     if i > entry.psl {
  //       break None
  //     }
  //     continue i + 1, (idx + 1) & self.capacity_mask
  //   }
  //   None => break None
  // }
  match a {
    Some(a) => println("a, \{a}!!!")
    None => println("a, None!!!")
  }
  let items = [1, 9, 46]
  items.push(99)
  // items.map(|x| println("x, \{x}!!!"))

  // if is expression
  let xx = if map.contains("w") { "w" } else { "no w" }
  println("xx, \{xx}!!!")

  // pipeline op.
  println(3 |> addOne |> addOne |> addOne)

  // https://docs.moonbitlang.com/#for-loop
  let sum = for i = 1, acc = 0; i <= 6; i = i + 1 {
    if i % 2 == 0 {
      println("even: \{i}")
      continue i + 1, acc + i
    }
  } else {
    acc
  }
  println(sum)

  // match
  let p : Int? = Some(1)
  println(p)
}
