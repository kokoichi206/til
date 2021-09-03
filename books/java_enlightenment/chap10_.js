let str = new String('foo');
console.log(typeof str);
str = 'foo';
console.log(typeof str);


let falseValue = new Boolean(false);
console.log(falseValue);
console.log(falseValue.valueOf());
console.log(falseValue.toString());
console.log(typeof falseValue);
if (falseValue) {
    console.log('falseValue is truthy');
}

let falsePrim = false;
console.log(typeof falsePrim);


let nullObject = null;
console.log(typeof nullObject); // CAUTION
console.log(nullObject === null);
console.log(nullObject === undefined);
console.log(nullObject == undefined);
