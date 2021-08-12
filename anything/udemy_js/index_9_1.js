console.log('%c [JavaScript]オブジェクト２'
, 'color:red; font-size: 1.5em');

function Person(first, last){
    this.first = first;
    this.last = last;
}

function Japanese(first, last){
    // this をバインドしている
    Person.call(this, first, last);
    this.lang = 'ja';
}

// prototypeも継承させる
Object.setPrototypeOf(Japanese.prototype, Person.prototype);

Person.prototype.introduce = function() {
    console.log('My name is ' + this.first + ' ' + this.last);
}

Japanese.prototype.sayJapanese = function() {
    console.log('こんちゃす' + this.first + ' ' + this.last);
}

let me = new Japanese('First', 'Last');
me.introduce();
