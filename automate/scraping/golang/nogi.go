package main

import (
	"net/http"
	"fmt"

	"github.com/PuerkitoBio/goquery"
)

const (
	BaseUrl = "https://www.nogizaka46.com/member/"
	// BaseUrl = "https://rooter.jp/web-crawling/go_goquery_scraping/"
)

func main() {
	// リクエストを作る
	req, err := http.NewRequest("GET", BaseUrl, nil)
	if err != nil {
		panic(err)
	}
	req.Header.Add("User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1")

	// リスエスト投げてレスポンスを得る
	client := &http.Client{}
	resp, err := client.Do(req)

	fmt.Println(resp)

	// レスポンスをNewDocumentFromResponseに渡してドキュメントを得る
	doc, err := goquery.NewDocumentFromResponse(resp)
	if err != nil {
		panic(err)
	}
	fmt.Println(doc)

	doc.Find("span.sub").Each(func(i int, s *goquery.Selection) {
		fmt.Println(s.Text())
		fmt.Println(s)
	})
}
