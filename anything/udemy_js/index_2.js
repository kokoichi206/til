console.log('%c [JavaScript]call, apply, bind の使い方'
    , 'color:red; font-size: 1.5em');

function greet() {
    console.log(this.name);
    console.log(arguments);
    let slicedArray = [].slice.call(arguments, 0,1);
    console.log(slicedArray);
}

let obj = {name: "Tom"};

greet.call(obj, 1,2,3);
// arguments が配列かどうかの違いだけ
greet.apply(obj, [1,2,3]);

const arry = [1,2,3,4];
console.log(Math.min.apply(null, arry));
console.log(Math.min(...arry));

let myObj = {
    id: 42,
    print() {
        console.log(this);
        // setTimeout は windowの関数
        // 
        setTimeout(function () {
            console.log(this);
        }.bind(this), 1000);
    }
}
