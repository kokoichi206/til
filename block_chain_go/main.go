package main

import (
	"log"
	"fmt"
	"blockchaingo/wallet"
)

func init() {
	log.SetPrefix("Blockchain: ")
}

func main() {
	w := wallet.NewWallet()
	fmt.Println(w.PublicKey())
	fmt.Println(w.PrivateKeyStr())
}
