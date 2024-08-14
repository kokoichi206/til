package main

import (
	"fmt"
	"net/http"
)

func main() {
	host := "localhost"
	// host := "0.0.0.0"
	// host := "127.0.0.1"
	port := 8080
	addr := fmt.Sprintf("%s:%d", host, port)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Headers", "*")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

		fmt.Fprintf(w, "Hello, World!")
	})

	fmt.Printf("Server is running on http://%s\n", addr)
	http.ListenAndServe(addr, nil)
}
