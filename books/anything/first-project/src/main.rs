fn main() {
    println!("Hello, world!");

    let t: (i32, &str) = (120, "文字列");

    let _t0 = t.0;
    let _t1 = t.1;

    if _t0 == 120 {
        println!("same value!!");
    }

    let _string: String = String::from(_t1);
    println!("{}", _string);

    for i in 0..10 {
        println!("in for-loop: {}", i);
    }

    let mut count = 0;
    while count < 10 {
        count += 1  // count++ のような書き方はできない
    }
    println!("count is {}", count);

    let banana = Fruit {
        name: String::from("Banana"),
    };
    println!("{}", banana.get_name());

    let _unit = Unit;
}

struct Fruit {
    name: String,
}

impl Fruit {
    fn get_name(&self) -> &str {
        &self.name
    }
}

struct Rectangle(i32, i32);

impl Rectangle {
    fn calc_area(&self) -> i32 {
        self.0 * self.1
    }
}

struct Unit;

trait Greeter {
    fn greet(&self);
}

struct Person(String);

impl Greeter for Person {
    fn greet(&self) {
        println!("Hello, I am {}!", self.0);
    }
}
