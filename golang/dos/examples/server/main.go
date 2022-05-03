package main

import (
	"fmt"
	"net/http"
	"time"


)

func test() {
	gohttp
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	
	// time.Sleep(10 * time.Second)
	time.Sleep(2 * time.Second)
	fmt.Fprint(w, "hello world")
}

func main() {
	http.HandleFunc("/", rootHandler)
	http.ListenAndServe(":8080", nil)
}
