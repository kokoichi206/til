let cody = new Object();
cody.living = true;
cody.age = 25;
cody.gender = 'male';
cody.getGender = function(){ return cody.gender }

console.log(cody.getGender());


let myObject = new Object();
myObject['0'] = 'f';
myObject['1'] = 'o';
myObject['2'] = 'o';

console.log(myObject);

let myString = new String('foo');

console.log(myString);


let objectFoo = {same: 'same'};
let objectBar = {same: 'same'};

console.log(objectFoo == objectBar);

let objectA = {foo: 'bar'};
let objectB = objectA;

console.log(objectA == objectB);

objectA.foo = 'foo';
console.log(objectB);


let objA = {property: 'value'};
let pointer1 = objA;
let pointer2 = pointer1;

objA.property = null;

console.log(objA.property, pointer1.property, pointer2.property);
