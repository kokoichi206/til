let cody = new Object();

for (key in cody) {
    if (cody.hasOwnProperty(key)) {
        console.log(key);
    }
}

Object.prototype.foo = 'foo';
let myString = 'bar';
// being found at Object.prototype.foo via prototype chain
console.log(myString.foo);
