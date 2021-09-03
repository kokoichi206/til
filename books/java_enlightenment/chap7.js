// function func1() {
//     setTimeout(function printfunc() {
//         console.log(this);
//     }, 500);
    
// }
// func1();

// function func2() {
//     setTimeout(() => {
//         console.log(this);
//     }, 500);
// }
// func2();


let countUpFromZero = function() {
    let count = 0;
    return function() {
        return ++count;
    };
}();    // invoke immediately, return nested function

console.log(countUpFromZero());
console.log(countUpFromZero());
console.log(countUpFromZero());
