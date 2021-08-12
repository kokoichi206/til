console.log('%c [JavaScript]オブジェクト'
, 'color:red; font-size: 1.5em');

// prototype が肝

// // __proto__ (prototype)が重要！
// let obj = {};
// obj.name = "Tom";
// obj.age = 34;
// let array = new Array();
// obj.arry = ["1", 1];
// console.log(obj);
// obj.obj = {name: "John"};

// ファクトリ関数
function factoryPerson(first, last){ // 名前すこ
    // こんな書き方できるんや
    let person = {first, last};
    return person;
}

let me = factoryPerson('First', 'Last');
console.log(me);

// コンストラクタ関数の場合は、先頭を大文字にする
function Person(first, last){
    this.first = first;
    this.last = last;
    // this.introduce = function() {
    //     console.log('My name is ' + first + ' ' + last);
    // }
}
Person.prototype.introduce = function() {
    console.log('My name is ' + this.first + ' ' + last);
}
// コンストラクタ関数の場合は、newで初期化する
let mee = new Person('First', 'Last');
let me1 = new Person('Me1', 'Desu');
// mee.introduce = function() {
//     console.log("I don't wanna introduce myself");
// }
// インスタンス化した後は、__proto__でアクセス, あんまり勧められてない書き方
mee.__proto__.introduce = function() {
    console.log("I don't wanna introduce myself");
}
mee.introduce();
me1.introduce();
