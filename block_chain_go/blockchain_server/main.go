package main

import (
	"flag"
	"log"
)

func init() {
	log.SetPrefix("Blockchain: ")
}

func main() {
	// Usage: go run main.go -port 5001
	port := flag.Uint("port", 5000, "TCP Port Number for Blockchain Server")
	flag.Parse()
	app := NewBlockchainServer(uint16(*port))
	app.Run()
}
