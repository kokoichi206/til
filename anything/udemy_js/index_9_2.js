//
// class
// ES6 から、クラス演算子が導入された！
// 中身としては 9_1 と変わらない
//
class Person {
    constructor(first, last) {
        this.first = first;
        this.last = last;
    }

    introduce() {
        console.log('My name is ' + this.first + ' ' + this.last);
    }
}

class Japanese extends Person {
    constructor(first, last) {
        super(first, last);
        this.lang = 'ja';
        this._age = 0;  // _ はプライベート変数であることを明示的にしてる
    }

    // 簡単にオーバーライドできる, プロトタイプチェーンに積まれるのか！
    introduce() {
        console.log('こんにちは！' + this.first + ' ' + this.last);
    };

    static sayHello() {
        console.log('こんにちは');
    }

    // set age(value) {
    //     this._age = value;
    // }
    // get age() {
    //     return this._age;
    // }

    set setAge(value) {
        this._age = value;
    }
    get getAge() {
        return this._age;
    }
}

let me = new Japanese('First', 'Last');
me.introduce();
// staticをつけると、インスタンス化しなくても使える
Japanese.sayHello();

// console.log(me.age);
// me.age = 10;
// console.log(me.age);
console.log(me.getAge);
me.setAge = 10;
console.log(me.getAge);


// // ES2019
// class ES2019 {
//     // 外部からアクセスできない！
//     #version = 2019;

//     set version(val) {
//         this.#version = val;
//     }

//     get version() {
//         return this.#version;
//     }

//     #increment() {
//         this.#version++;
//     }
//     printVersion() {
//         this.#increment();
//         console.log(`%cHi, my version is %c${this.#version}`, 'font-size:1.5em; color:red', 'font-size:1.5em; color:green')
//     }
// }
// const es = new ES2019();
// es.printVersion();
// // console.log(es.#version);
