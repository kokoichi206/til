package main

import (
	"fmt"
)

func main() {
	// nil は必ずアクセスに失敗し、ページフォルトが発生する特殊なメモリアクセス！！
	var p *int = nil
	fmt.Println("不正メモリアクセス前")
	*p = 0
	fmt.Println("不正メモリアクセス後")

	// // not working...
	// ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGSEGV)
	// defer stop()
	// // nil は必ずアクセスに失敗し、ページフォルトが発生する特殊なメモリアクセス！！
	// var p *int = nil
	// fmt.Println("不正メモリアクセス前")
	// *p = 0
	// fmt.Println("不正メモリアクセス後")

	// <-ctx.Done()
}
