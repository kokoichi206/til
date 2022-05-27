package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

// while; do go run main.go && sleep 10; done
func main() {
	url := "https://kokoichi0206.mydns.jp/"
	GetHTML(url)
}

func GetHTML(url string) {
	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		panic(err)
	}

	req.Header.Add("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3864.0 Safari/537.36")
	client := &http.Client{}

	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("failed to get response: %v", err)
		return
	}
	defer resp.Body.Close()

	// var blog model.BlogList
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("failed to read response: %v", err)
		return
	}
	fmt.Println(string(body))
}
