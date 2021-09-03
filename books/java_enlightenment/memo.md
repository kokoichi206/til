## Preface
- More code, less words
  - I hope you achieve a level of expertise such that well-documented code is all you need to grok a programming concept.
- Exhaustive code and repetition


## chap 1
In JavaScript, objects are king:

Object() object

Primative values like "foo", 5 and true are the exception but have equivalent wrapper objects

To drive this fact home, examine and contrast the code below.

### Primative values
Primitive values are copied literally.

Primative values are equal by value.

Complex objects are equal by reference

The big take away here is that when you change a complex value - because it is stored by reference = you change the value stored in all variables that reference that complex value.


## chap 3
prototype chain

## chap 5
This "window" object is considered to be the "head object", or sometimes confusingly referred to as "the global object"

## chap 7
The scop chain lookup returns the first found value

Scope is determined during function definition, not invocation.

Closures are caused by the scope chain

```javascript
let countUpFromZero = function() {
    let count = 0;
    return function() {
        return ++count;
    };
}();    // invoke immediately, return nested function

console.log(countUpFromZero());
console.log(countUpFromZero());
console.log(countUpFromZero());
```

Each time the coutUpFromZero function is invoked, the anonymous function contained in (and returned from) the countUpFromZero function still has access to the parent function's scope. This technique, facilitated via the scope chain, is an example of a closure.


## chap 8
The prototype property is an object created by JS for every Function() instance.

Last stop in the prototype chain is Object.prototype


## chap 9
What you need to know is that arrays are numerically ordered sets, versus objects, which have property names associated with values in non-numeric order.


## chap 10-
Primitive/literal values are converted to objects when properties are accessed

wrapper object

The key thing to grok here is what is occurring, and that JavaScript is doing this for you behind the scenes.

You should typically use primitive string, number, and boolean values


## Words
- pertain
- ready-to-usev
- lexical scoping
- leverage
