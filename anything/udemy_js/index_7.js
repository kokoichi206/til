console.log('%c [JavaScript]非同期処理'
, 'color:red; font-size: 1.5em');

// // js はもともと非同期処理を念頭に開発された言語
// function wait(callback, num) {
//     setTimeout(() => {
//         console.log(num);
//         callback(num);
//     }, 100);
// }
// // callback 地獄
// wait(num => {
//     num++;
//     wait(num => {
//         num++;
        
//     }, num);
// }, 0);

// function waitpro(num) {
//     return new Promise((resolve, reject) => {
//         setTimeout(() => {
//             console.log(num);
//             if(num === 2){
//                 reject(num);
//             } else {
//                 resolve(num);
//             }
//         }, 100);
//     })
// }
// waitpro(0).then(num => {
//     num++;
//     // thenメソッドでチェーンを繋ぎたい場合は、returnでPromiseを返すようにする
//     return waitpro(num);
// }).then(num => {
//     num++;
//     return waitpro(num);
// }).catch(num => {
//     num++;
//     console.error(num, 'error');
// })


// //` 非同期処理を並列で走らせたい時！ Promise.all()
// function wait2(num) {
//     return new Promise((resolve, reject) => {
//         setTimeout(() => {
//             console.log(num);
//             resolve(num);
//         }, num);
//     })
// }
// Promise.all([wait2(1000), wait2(1500), wait2(2000)]).then(nums => {
//     console.log(nums);
// })


// await, async は Promise よりも直感的な記述が可能なもの
function wait3(num) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            console.log(num);
            if(num === 2){
                reject(num);
            }else{
                resolve(num);
            }
        }, 100);
    })
}

async function init() {
    // Promiseで返すものを await で受けとれる
    // await の場合は try, catch でエラーを受ける
    let num = 0;
    try {
        // ここでletだと、letでスコープができちゃう
        num = await wait3(0);
        num++;
        num = await wait3(num);
        num++;
        num = await wait3(num);
        num++;
    }catch(e){
        throw new Error('Error is occured', e);
    }
    return num;
}
// Promiseがかえる
// console.log(init());
init().then(num => {
    console.log('End');
})
