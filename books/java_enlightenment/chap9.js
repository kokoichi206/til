let foo = new Array(1, 2, 3);
let bar = new Array(100); // CAUTION:

console.log(foo[0], foo[2]);
console.log(bar[0], bar.length);

// let myArray = [];
// let myArray = new Array(5555553535353535);   // ERROR
let myArray = new Array();
let MIDIUM_NUM = 53535;
myArray[MIDIUM_NUM] = 'baka';
let LARGE_NUM = 5555553535353535;
myArray[LARGE_NUM] = 'baka';
myArray[50] = 'blue';
console.log(myArray);
console.log(myArray.length);
console.log(myArray[6]);
console.log(typeof myArray);
