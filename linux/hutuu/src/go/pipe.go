package main

import (
	"fmt"
	"os"
	"os/exec"
	"syscall"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintf(os.Stderr, "Usage: %s <command1> <command2>\n", os.Args[0])
		os.Exit(1)
	}

	rfd, wfd, err := os.Pipe()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Pipe creation failed: %v\n", err)
		os.Exit(1)
	}

	path1, err := exec.LookPath(os.Args[1])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to find %s: %v\n", os.Args[1], err)
		os.Exit(1)
	}

	pid, err := syscall.ForkExec(path1, []string{os.Args[1]}, &syscall.ProcAttr{
		Dir:   ".",
		Env:   os.Environ(),
		Files: []uintptr{os.Stdin.Fd(), uintptr(wfd.Fd()), os.Stderr.Fd()},
		Sys:   nil,
	})
	if err != nil {
		fmt.Fprintf(os.Stderr, "ForkExec failed: %v\n", err)
		os.Exit(1)
	}

	wfd.Close()

	path2, err := exec.LookPath(os.Args[2])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to find %s: %v\n", os.Args[2], err)
		os.Exit(1)
	}

	syscall.Dup3(int(rfd.Fd()), int(os.Stdin.Fd()), 0)
	rfd.Close()

	err = syscall.Exec(path2, []string{os.Args[2]}, os.Environ())
	if err != nil {
		fmt.Fprintf(os.Stderr, "Exec failed: %v\n", err)
		os.Exit(1)
	}

	syscall.Wait4(pid, nil, 0, nil)
}
