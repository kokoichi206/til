package main

import (
	"net/http"
	"fmt"

	// "github.com/PuerkitoBio/goquery"
)

const (
	BaseUrl = "https://kokoichi0206.mydns.jp/"
)

func main() {
	// リクエストを作る
	req, err := http.NewRequest("GET", BaseUrl, nil)
	if err != nil {
		panic(err)
	}

	// リスエスト投げてレスポンスを得る
	client := &http.Client{}
	resp, err := client.Do(req)

	fmt.Println(resp)

	req.Header.Add("User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1")

	// リスエスト投げてレスポンスを得る
	client = &http.Client{}
	resp, err = client.Do(req)

	fmt.Println(resp)
}
