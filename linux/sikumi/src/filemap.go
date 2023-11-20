package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"syscall"
)

// メモリマップトファイルを使ったファイルのデータ更新。
func main() {
	pid := os.Getpid()
	// echo hello > testfile
	fmt.Println("======== testfile のメモリマップ前のプロセスの仮想アドレス空間 ========")
	command := exec.Command("cat", fmt.Sprintf("/proc/%d/maps", pid))
	command.Stdout = os.Stdout
	if err := command.Run(); err != nil {
		log.Fatal(err)
	}

	f, err := os.OpenFile("testfile", os.O_RDWR, 0)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	// mmap システムコールにより 5 bytes のメモリ領域を獲得！
	data, err := syscall.Mmap(int(f.Fd()), 0, 5, syscall.PROT_READ|syscall.PROT_WRITE, syscall.MAP_SHARED)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("\ntestfile をマップしたアドレス: %p\n\n", &data[0])

	fmt.Println("======== testfile のメモリマップ後のプロセスの仮想アドレス空間 ========")
	command = exec.Command("cat", fmt.Sprintf("/proc/%d/maps", pid))
	command.Stdout = os.Stdout
	if err := command.Run(); err != nil {
		log.Fatal(err)
	}

	// マップしたファイルの中身を置き換える。
	replaceBytes := []byte("HELLO")
	for i, _ := range data {
		data[i] = replaceBytes[i]
	}
}
