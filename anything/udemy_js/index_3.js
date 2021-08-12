console.log('%c [JavaScript]call, apply, bind の使い方'
, 'color:red; font-size: 1.5em');

let myObj = {
    id: 42,
    print() {
        console.log(this);
        let _this = this;
        setTimeout(function () {
            console.log(_this);
        }, 1000);
    }
}
myObj.print();
let myObj2 = {
    id: 42,
    print() {
        console.log(this);
        // アロー関数は this を作らない
        // thisが見つからないので、
        // スコープチェーンをたどって探しに行く
        setTimeout(() => {
            console.log(this);
        }, 1000);
    }
}
myObj2.print();

// let me = 'global じゃないのか';
window.me = 'global';
const outer = function() {
    let me = 'outer';

    return {
        me: 'inner',
        say: () => {
            console.log(this.me);
        }
    }
}
outer().say();
