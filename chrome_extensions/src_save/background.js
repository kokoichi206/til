chrome.contextMenus.create({
    "title" : "検索した語句を表示",
    "type"  : "normal",
    "contexts" : ["all"],
    "onclick" : () => {
        chrome.storage.sync.get(/* String or Array */["searchWords"], function(items){
            //  items = [ { "yourBody": "myBody" } ]
;
            console.log(items);
        });
        let url = "https://www.google.co.jp/"
        chrome.tabs.create({ url : url});
    }
});