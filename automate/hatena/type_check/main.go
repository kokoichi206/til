package main

import (
	"encoding/json"
	"fmt"
	"strings"
)

type Article struct {
	Category []string
}

func main() {
	var ar Article
	jsonString := `{"Category":"Android"}`

	// string は []string としてデコードしてくれないのでエラーになる。
	if err := json.NewDecoder(strings.NewReader(jsonString)).Decode(&ar); err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("%+v\n", ar)
}
