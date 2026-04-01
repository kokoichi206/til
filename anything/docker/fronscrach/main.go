package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"syscall"
)

// docker 		  run image <cmd> <params>
//
// go run main.go run       <cmd> <params>

func main() {
	switch os.Args[1] {
	case "run":
		run()
	case "child":
		child()
	default:
		panic("bad command")
	}
}

func run() {
	fmt.Printf("Running %v as %d\n", os.Args[2:], os.Getpid())

	// need sudo to run.
	cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	cmd.SysProcAttr = &syscall.SysProcAttr{
		// New utsname namespace.
		Cloneflags: syscall.CLONE_NEWUTS |
			syscall.CLONE_NEWPID |
			syscall.CLONE_NEWNS,
		Unshareflags: syscall.CLONE_NEWNS,
	}

	if err := cmd.Run(); err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
}

func child() {
	fmt.Printf("Running %v as %d\n", os.Args[2:], os.Getpid())

	_, cleanup := cg()
	defer cleanup()

	syscall.Sethostname([]byte("container"))
	syscall.Chroot("/container/testing-fs")
	syscall.Chdir("/")

	syscall.Mount("proc", "proc", "proc", 0, "")

	cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}

	syscall.Unmount("proc", 0)
}

// cgroup v2 の例。
func cg() (string, func()) {
	base := "/sys/fs/cgroup"
	// ls /sys/fs/cgroup/kk
	group := filepath.Join(base, "kk")

	// 親で pids controller を子に有効化
	must(os.WriteFile(filepath.Join(base, "cgroup.subtree_control"), []byte("+pids"), 0644))

	// 子 cgroup 作成
	if _, err := os.Stat(group); os.IsNotExist(err) {
		must(os.Mkdir(group, 0755))
	}

	// 制限設定
	// 	sh-5.3# cat /sys/fs/cgroup/kk/pids.max
	// 20
	//
	// :() { : | : & }; :
	must(os.WriteFile(filepath.Join(group, "pids.max"), []byte("20"), 0644))

	// 自プロセスを移動
	must(os.WriteFile(filepath.Join(group, "cgroup.procs"), []byte(strconv.Itoa(os.Getpid())), 0644))

	// cleanup 関数返す
	cleanup := func() {
		// 念のためプロセスを親に戻す
		must(os.WriteFile(filepath.Join(group, "cgroup.procs"), []byte("0"), 0644))

		// 削除
		if err := os.Remove(group); err != nil {
			fmt.Printf("cleanup failed: %v\n", err)
		}
	}

	return group, cleanup
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}
