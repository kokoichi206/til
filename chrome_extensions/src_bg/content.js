// window.alert('アプリ開いたね！');

const imageURL = chrome.extension.getURL('renka.png');
document.getElementsByTagName("body")[0].style.backgroundImage = `url(${imageURL})`;

