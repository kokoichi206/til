console.log('%c [JavaScript]ループを使いこなそう'
, 'color:red; font-size: 1.5em');

const data = [1, 4, 2, 5, 3];
const fruits = {banana: 'バナナ', apple: 'りんご', orange: 'オレンジ'};

Object.prototype.additionlFn = function(){};

let keyFruits = Object.keys(fruits);

for(let i in fruits){
    // objectのprototypeを参照しに行くので、変なことにならないよう、
    // hasOwnpropertyかを確かめるのが一般的
    // プロトタイプ継承させないようにする
    if(fruits.hasOwnProperty(i)){
        console.log(i, fruits[i]);
    }    
}

for(let i in data){
    if(data.hasOwnProperty(i)){
        console.log(i, data[i]);
    }    
}

for(let i of keyFruits) {
    console.log(i, fruits[i]);
}

// ES8 以上
let keyentries = Object.entries(fruits);
for(let [k, v] of keyentries) {
    console.log(k, v);
}


// higher order function
// 高階関数
// functionを引数に持ったり、関数を戻り値にもったりするもの
data.forEach((value, index, array) => {
    console.log(value, index, array);
});

const newData = data.map((value, index, array) => {
    return value * 2;
})
console.log('data', data);
console.log('newData', newData);

const filterData = data.filter((value, index, array) => {
    return value !== 1;
})
console.log('filterData', filterData);

const accumulate = data.reduce((accu, curr) => {
    console.log(accu, curr)
    return accu + curr;
})
console.log('reduce', accumulate);

const sortData = data.sort((a, b) => {
    return a - b;
})
console.log('sortedData', sortData);

// 高階関数を利用したループをお勧めする理由！
// メソッドチェーンが使える！！！
// 実際の処理のところが配列の内容と切り離されているので、
// 処理の内容が明確になりやすい
const chain = data
.map(v => v + 1)
.sort((a, b) => {
    return a - b;
})
console.log('chain', chain);
