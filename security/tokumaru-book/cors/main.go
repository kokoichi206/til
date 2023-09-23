package main

import (
	"fmt"
	"net/http"
)

const frontOrigin = "http://localhost:8050"

// preFlight で許可されないパターン（403 を返す）。
func preFlightNG(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusForbidden)
		return
	}

	w.WriteHeader(http.StatusOK)
}

// preFlight で許可されるが、実際のリクエストで許可されないパターン（Allow ヘッダー不足）。
func preFlightOK(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPatch:
		w.WriteHeader(http.StatusOK)
	case http.MethodOptions:
		if r.Header.Get("Origin") != frontOrigin {
			w.WriteHeader(http.StatusForbidden)
			return
		}
		// フロントエンドのドメインを指定する。
		w.Header().Set("Access-Control-Allow-Origin", frontOrigin)
		w.Header().Set("Access-Control-Allow-Methods", "PATCH")
		w.Header().Set("Access-Control-Max-Age", "10")
		w.WriteHeader(http.StatusOK)
	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

// preFlight で許可され、実際のリクエストでも許可されるパターン。
func corsOK(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPatch:
		w.Header().Set("Access-Control-Allow-Origin", frontOrigin) // preFlightOK Handler との差分。
		w.WriteHeader(http.StatusOK)
	case http.MethodOptions:
		if r.Header.Get("Origin") != frontOrigin {
			w.WriteHeader(http.StatusForbidden)
			return
		}
		// フロントエンドのドメインを指定する。
		w.Header().Set("Access-Control-Allow-Origin", frontOrigin)
		w.Header().Set("Access-Control-Allow-Methods", "PATCH")
		w.Header().Set("Access-Control-Max-Age", "10")
		w.WriteHeader(http.StatusOK)
	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

func serveFront() {
	mux := http.NewServeMux()
	mux.HandleFunc("/patch", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, `
			<!DOCTYPE html>
			<html lang="ja">
			<head>
				<meta charset="UTF-8">
				<title>Go HTML</title>
			</head>
			<body>
				<script>
					fetch('http://localhost:7171/pre-ng', {method: 'PATCH'})
					fetch('http://localhost:7171/pre-ok', {method: 'PATCH'})
					fetch('http://localhost:7171/cors-ok', {method: 'PATCH'})
				</script>
				<h1>Hello, Golang!</h1>
			</body>
			</html>
		`)
	})

	http.ListenAndServe(":8050", mux)
}

func main() {
	go serveFront()

	mux := http.NewServeMux()
	mux.HandleFunc("/pre-ng", preFlightNG)
	mux.HandleFunc("/pre-ok", preFlightOK)
	mux.HandleFunc("/cors-ok", corsOK)

	fmt.Println("http://localhost:8050/patch")
	if err := http.ListenAndServe(":7171", mux); err != nil {
		panic(err)
	}
}
