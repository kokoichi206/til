const notifyURLChange = (tabId: number, url: string) => {
  chrome.tabs.sendMessage(tabId, { type: "urlChange", url }, (response) => {
    if (chrome.runtime.lastError) {
      console.error(
        "Error sending message to content script:",
        chrome.runtime.lastError.message
      );
    } else {
      console.log("Response from content script:", response);
    }
  });
};

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  console.log("changeInfo.status: ", changeInfo.status);
  if (changeInfo.status === "complete" && tab && tab.url) {
    console.log("tabId: ", tabId);
    console.log("changeInfo: ", changeInfo);

    if (tab) {
      notifyURLChange(tabId, tab.url?.toString() || "");
    }
  }
});

chrome.runtime.onMessage.addListener((message, _sender, _sendResponse) => {
  if (message.type === "sendDOMData") {
    // 受け取ったDOMデータを表示
    console.log("Received DOM data:", message.domData);
  }
});
