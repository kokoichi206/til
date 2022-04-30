package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	httpMethod := "GET"
	// url := "https://api.github.com"
	url := "http://localhost:8080"

	client := http.Client{}

	request, err := http.NewRequest(httpMethod, url, nil)

	// response, err := client.Get(url)

	request.Header.Set("Accept", "application/xml")

	response, err := client.Do(request)

	if err != nil {
		panic(err)
	}

	defer response.Body.Close()
	bytes, err := ioutil.ReadAll(response.Body)
	if err != nil {
		panic(err)
	}

	fmt.Println(response.StatusCode)
	fmt.Println(string(bytes))
}
