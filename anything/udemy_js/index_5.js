console.log('%c [JavaScript]スプレッド構文を使いこなそう'
, 'color:red; font-size: 1.5em');

function sum(x, y, z) {
    return x + y + z;
}

sum(1, 2, 3);

const numbers = [1,2,3];
console.log(sum(...numbers));
console.log(sum.apply(null, numbers));

let obj1 = { foo: 'bar', x: 21 };
let obj2 = { foo: 'baz', y: 52 };

let clonedObj = { ...obj1 };
let mergedObj = { ...obj1, ...obj2 };

console.log(clonedObj);
clonedObj.foo = 'foo';
console.log(obj1);
console.log(mergedObj);

// スプレッド構文を使う上での注！
// １段階目のみ値わたしで、２段階目以降は参照！
let a = [[1], [2], [3]];
let b = [...a];
b.shift().shift();
console.log(b);
console.log(a);

// Rest Parameters
function sum(...theArgs) {
    return theArgs.reduce((previous, current) => {
        return previous + current;
    });
}

function f(a, ...args) {
    console.log(args);
}
f(1,2,3,4,5);
