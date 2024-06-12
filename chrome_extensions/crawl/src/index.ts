// メッセージを受信するリスナーを設定
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === "urlChange") {
    console.log("urlChange:", message.url);
    // APIデータを処理する
  } else if (message.type === "apiError") {
    console.error("Received API error:", message.error);
    // エラーを処理する
  }
  // 応答を送信
  sendResponse({ received: true });
});
