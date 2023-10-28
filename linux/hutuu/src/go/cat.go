package main

import (
	"fmt"
	"log"
	"os"
	"syscall"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "%s: file name was not given\n", os.Args[0])
		os.Exit(1)
	}

	for i := 1; i < len(os.Args); i++ {
		cat(os.Args[i])
	}
}

const BUFFER_SIZE = 2048

func cat(path string) {
	fd, err := syscall.Open(path, os.O_RDONLY, 0x755)
	if err != nil {
		log.Fatal(err)
	}

	var buf = make([]byte, BUFFER_SIZE)

	for {
		n, err := syscall.Read(fd, buf)
		if err != nil {
			log.Fatal(err)
		}

		if n == 0 {
			break
		}

		syscall.Write(int(os.Stdout.Fd()), buf[:n])
	}
}
