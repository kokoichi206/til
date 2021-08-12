console.log('%c [JavaScript]call, クロージャー'
, 'color:red; font-size: 1.5em');

// js に置いてプライベート変数を使いたい時に、クロージャを使う！！

// クロージャは、関数と、その関数が定義された
// レキシカルスコープの組み合わせです

// 即時関数で囲むと、定義された時点で実行される関数
let increment = (function () {

    // lexical scope とは、関数から見た親のスコープのこと 
    let counter = 0; // Lexical Scope

    // 戻り値の引数がレキシカルスコープを持っている
    // 外部からはcounterへのアクセスができないのが利点！！
    return function() {
        counter += 1;
        console.log(counter);
        // return counter
    }
})();
increment.counter = 10;
increment(); //1
increment(); //2
increment(); //3


function addStringFactory(tail) {
    // 内側の関数から外側の関数の変数（tail）への参照を持っている状態
    // function concat(str) {
    //     return str + tail;
    // }
    // return concat;
    return function(str) {
        return str + tail;
    }
}

let addAs = addStringFactory("AAAAAA");
let addBs = addStringFactory('BBBBBB');

let str = 'Tom';
str = addBs(str);
console.log(str);
