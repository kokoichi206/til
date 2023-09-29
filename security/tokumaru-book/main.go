package main

import (
	"fmt"
	"strconv"
)

func main() {
	// Null バイト。
	nullByteString := "Hello\x00World"

	// 文字列を出力
	fmt.Println(nullByteString)

	// 各バイトを出力
	for _, b := range nullByteString {
		fmt.Printf("%x ", b)
	}

	null := "\x00"
	a, err := strconv.ParseInt(null, 16, 32)
	fmt.Printf("a: %v\n", a)
	fmt.Printf("err: %v\n", err)
}
