package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"syscall"
)

const (
	ALLOC_SIZE = 1024 * 1024 * 1024
)

func main() {
	pid := os.Getpid()
	fmt.Println("新規メモリ領域獲得前のメモリマップ")
	command := exec.Command("cat", fmt.Sprintf("/proc/%d/maps", pid))
	command.Stdout = os.Stdout
	err := command.Run()
	if err != nil {
		log.Fatal(err)
	}

	// mmap() のシステムコールによって 1GB のメモリ領域を確保する。
	data, err := syscall.Mmap(-1, 0, ALLOC_SIZE, syscall.PROT_READ|syscall.PROT_WRITE, syscall.MAP_ANON|syscall.MAP_PRIVATE)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("新規メモリ領域: アドレス=%p, サイズ=%d\n", &data[0], len(data))
	fmt.Println("新規メモリ領域獲得後のメモリマップ")
	command = exec.Command("cat", fmt.Sprintf("/proc/%d/maps", pid))
	command.Stdout = os.Stdout
	err = command.Run()
	if err != nil {
		log.Fatal(err)
	}
}
