package main

import (
	_ "embed"
	"fmt"
	"net/http"
)

//go:embed cat.png
var cat []byte

func main() {
	// 正常。
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html")
		fmt.Fprintf(w, `<script src="/html/nosniff"></script>`)
		fmt.Fprintf(w, `<script src="/json/nosniff"></script>`)
		fmt.Fprintf(w, `<script src="/html"></script>`)
		fmt.Fprintf(w, `<script src="/json"></script>`)
		fmt.Fprintf(w, `<script src="/png"></script>`)
	})

	// 不正な Content-Type: text/html。
	// これで発生するのは本来おかしい！
	http.HandleFunc("/html", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html")
		fmt.Fprintf(w, `alert('hi from html');`)
	})

	// 不正な Content-Type: application/json。
	// これで発生するのは本来おかしい！
	http.HandleFunc("/json", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, `alert('hi from json');`)
	})

	// 不正な Content-Type: image/png。
	// これはエラーになる。
	http.HandleFunc("/png", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "image/png")
		fmt.Fprintf(w, `alert('hi from png');`)
	})

	// nosniff が設定されている。
	http.HandleFunc("/html/nosniff", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		fmt.Fprintf(w, `alert('hi from html with nosniff');`)
	})
	http.HandleFunc("/json/nosniff", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("X-Content-Type-Options", "nosniff")
		fmt.Fprintf(w, `alert('hi from json with nosniff');`)
	})

	port := 9999
	fmt.Printf("http://localhost:%d\n", port)
	http.ListenAndServe(fmt.Sprintf(":%d", port), nil)
}
