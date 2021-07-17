// window.alert('アプリ開いたね！');

console.log("オッケ");
// console.log(document.URL);
// console.log(document.URL.split("google.com/search?q="))

let queries = document.URL.split("google.com/search?q=")[1];
if( queries.length > 1 ){    
    let query = queries.split("&")[0];
    const rawQuery = decodeURI(query);
    
    // chrome.management.getAll(apps => {
    //     console.log(apps);
    // });

    const key = "searchWords"
    let items = localStorage[`${key}`];
    let array;
    if( items ){
        array = JSON.parse(items);
        array.push(rawQuery);
    } else {
        array = [rawQuery];
    }
    localStorage[`${key}`] = JSON.stringify(array);
    console.log('Value is set to ' + JSON.stringify(array));
    // chrome.storage.sync.get(/* String or Array */[key], function(items){
    //     //  items = [ { "yourBody": "myBody" } ]
    //     let newArray;
    //     console.log(items);
    //     if( items == {} ){
    //         console.log(here);
    //         let array = JSON.parse(items);
    //         console.log(array);
    //         newArray = array.push(rawQuery);
    //     } else {
    //         newArray = [rawQuery];
    //     }

    //     chrome.storage.sync.set({key: JSON.stringify(newArray)}, function() {
    //         console.log('Value is set to ' + newArray);
    //     });
    // });
}
