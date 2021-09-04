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
	fmt.Println(w.PrivateKeyStr())
	fmt.Println(w.PublicKey())
	fmt.Println(w.BlockchainAddress())
}
