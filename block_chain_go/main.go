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

	// トランザクションのストラクチャーを作る
	t := wallet.NewTransaction(w.PrivateKey(), w.PublicKey(), w.BlockchainAddress(), "B", 1.0)
	fmt.Printf("signature %s\n", t.GenerateSignature())
}
