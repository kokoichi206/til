package main

import (
	"github.com/kokoichi206/go-http-client/gohttp"
)

// "github.com/kokoichi206/go-http-client/gohttp"
// "github.com/federicoleon/go-httpclient/gohttp"

var (
	httpClient = gohttp.NewBuilder().Build()
)

func main() {
	gohttp.NewBuilder().
		SetUserAgent("").
		SetHeaders(nil)

	response, err := httpClient.Get("https://api.github.com")
	if err != nil {
		panic(err)
	}
	print(response.StatusCode())
	print(response.String())
}
