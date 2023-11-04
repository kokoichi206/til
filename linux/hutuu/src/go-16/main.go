package main

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"log"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"syscall"
	"time"
)

const (
	SERVER_NAME             = "LittleHTTP"
	SERVER_VERSION          = "1.0"
	HTTP_MINOR_VERSION      = 0
	BLOCK_BUF_SIZE          = 1024
	LINE_BUF_SIZE           = 4096
	MAZ_REQUEST_BODY_LENGTH = 1024 * 1024
)

type HTTPHeaderField struct {
	name  string
	value string
	next  *HTTPHeaderField
}

type HTTPRequest struct {
	protocolMinorVersion int
	method               string
	path                 string
	header               *HTTPHeaderField
	body                 *string
	length               int64
}

type FileInfo struct {
	path *string
	size int64
	ok   int
}

func logExit(format string, args ...any) {
	fmt.Fprintf(os.Stderr, format, args...)
	os.Exit(1)
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintf(os.Stderr, "Usage: %s <docroot>\n", os.Args[0])
		os.Exit(1)
	}

	sigs := make(chan os.Signal, 1)
	ctx, cancel := context.WithCancel(context.Background())
	defer func() {
		// シグナルの受付を終了する
		signal.Stop(sigs)
		cancel()
	}()

	installSignalHandlers(sigs)

	go func() {
		select {
		case sig := <-sigs: // シグナルを受け取ったらここに入る
			fmt.Println("Got signal!", sig)
			cancel() // cancelを呼び出して全ての処理を終了させる
		}
	}()

	service("/dev/stdin", "/dev/stdout", os.Args[1])

	ctx.Done()
}

func installSignalHandlers(sigs chan<- os.Signal) {
	// ソケットが切断されると SIGPIPE が飛んでくる。
	signal.Notify(sigs, syscall.SIGPIPE)
}

func service(in, out string, docroot string) {
	var req *HTTPRequest

	// os.Stdin の定義。
	inFile := os.NewFile(uintptr(syscall.Stdin), in)
	req = readRequest(inFile)

	// fmt.Printf("req: %+v\n", req)
	// fmt.Printf("req.header: %+v\n", req.header)

	outFile := os.NewFile(uintptr(syscall.Stdin), in)
	writer := bufio.NewWriter(outFile)

	respondTo(req, writer, docroot)
}

func readRequest(in io.Reader) *HTTPRequest {
	var req *HTTPRequest = &HTTPRequest{}
	var h *HTTPHeaderField = &HTTPHeaderField{}

	// req.header = h

	reader := bufio.NewReader(in)

	readRequestLine(req, reader)
	for {
		h = readHeaderField(reader)
		if h == nil {
			break
		}

		// 過去の header を新規 header の next に設定する。
		h.next = req.header
		req.header = h
	}

	req.length = contentLength(req)

	return req
}

func readRequestLine(req *HTTPRequest, reader *bufio.Reader) {

	buf, err := reader.ReadString('\n')
	if err != nil {
		log.Fatal("no request line")
	}

	buf = strings.TrimSpace(buf)
	parts := strings.SplitN(buf, " ", 3)
	if len(parts) < 3 {
		log.Fatalf("parse error on request line: %s", buf)
	}

	req.method = strings.ToUpper(parts[0])

	req.path = parts[1]

	if !strings.HasPrefix(parts[2], "HTTP/1.") {
		log.Fatalf("parse error on request line (3): %s", buf)
	}
	protoParts := strings.SplitN(parts[2], "/", 2)
	if len(protoParts) < 2 {
		log.Fatalf("parse error on request line (3): %s", buf)
	}
	verParts := strings.SplitN(protoParts[1], ".", 2)
	if len(verParts) < 2 {
		log.Fatalf("parse error on request line (3): %s", buf)
	}
	req.protocolMinorVersion, err = strconv.Atoi(verParts[1])
	if err != nil {
		log.Fatalf("parse error on request line (3): %s", buf)
	}
}

func readHeaderField(reader *bufio.Reader) *HTTPHeaderField {
	buf, err := reader.ReadString('\n')
	if err != nil {
		if err == io.EOF {
			// EOFはヘッダーの終わりを意味する可能性がある。
			return nil
		}
		logExit("failed to read request header field: %v", err)
	}

	// リクエストが終了したことを示す空行を検出
	if buf == "\n" || buf == "\r\n" {
		return nil
	}

	parts := strings.SplitN(buf, ":", 2)
	if len(parts) != 2 {
		logExit("parse error on request header field: %s", buf)
	}

	name := strings.TrimSpace(parts[0])
	value := strings.TrimSpace(parts[1])

	return &HTTPHeaderField{
		name:  name,
		value: value,
	}
}

func contentLength(req *HTTPRequest) int64 {
	val := lookupHeaderFieldValue(req, "Content-Length")
	if val == "" {
		return 0
	}
	len, err := strconv.ParseInt(val, 10, 64)
	if err != nil || len < 0 {
		logExit("negative Content-Length value or parsing error: %v", err)
	}
	return len
}

func lookupHeaderFieldValue(req *HTTPRequest, name string) string {
	for h := req.header; h != nil; h = h.next {
		if strings.EqualFold(h.name, name) {
			return h.value
		}
	}
	return ""
}

func respondTo(req *HTTPRequest, w *bufio.Writer, docroot string) {
	switch req.method {
	case "GET":
		doFileResponse(req, w, docroot)
	case "HEAD":
		doFileResponse(req, w, docroot)
	}

	// TODO:
}

// ファイル応答を生成する関数です。
func doFileResponse(req *HTTPRequest, w *bufio.Writer, docroot string) {
	path := buildPath(docroot, req.path)

	var fs syscall.Stat_t
	if err := syscall.Stat(path, &fs); err != nil {
		fmt.Printf("err: %v\n", err)
		// TODO:
		return
	}

	// fmt.Printf("fs: %+v\n", fs)

	outputCommonHeaderFields(req, w, "200 OK")

	fmt.Fprintf(w, "Content-Length: %d\r\n", fs.Size)
	fmt.Fprintf(w, "Content-Type: %s\r\n", guessContentType(&fs))
	fmt.Fprintf(w, "\r\n")

	if req.method != "HEAD" {
		fd, err := syscall.Open(path, os.O_RDONLY, fs.Mode)
		if err != nil {
			// TODO:
			fmt.Printf("err: %v\n", err)
			return
		}

		buf := make([]byte, 4096)
		n, err := syscall.Read(fd, buf)
		if err != nil {
			// TODO:
			fmt.Printf("err: %v\n", err)
			return
		}

		syscall.Close(fd)

		w.Write(buf[:n])
	}

	w.Flush()
}

func outputCommonHeaderFields(req *HTTPRequest, out *bufio.Writer, status string) {
	t := time.Now().UTC()             // 現在時刻を取得し、UTCに変換
	dateStr := t.Format(time.RFC1123) // RFC1123形式にフォーマット

	// var st syscall.Time_t
	// syscall.Time(&st)
	// fmt.Printf("st: %v\n", st)

	_, err := fmt.Fprintf(out, "HTTP/1.%d %s\r\n", req.protocolMinorVersion, status)
	if err != nil {
		logExit("failed to write status line: %v", err)
	}
	_, err = fmt.Fprintf(out, "Date: %s\r\n", dateStr)
	if err != nil {
		logExit("failed to write date: %v", err)
	}
	_, err = fmt.Fprintf(out, "Server: %s/%s\r\n", SERVER_NAME, SERVER_VERSION)
	if err != nil {
		logExit("failed to write server: %v", err)
	}
	_, err = fmt.Fprintf(out, "Connection: close\r\n")
	if err != nil {
		logExit("failed to write connection: %v", err)
	}
}

func guessContentType(fs *syscall.Stat_t) string {
	// FIXME:
	return "text/plain"
}

func buildPath(docroot, path string) string {
	if path[0] == '/' {
		return fmt.Sprintf("%s%s", docroot, path)
	}

	return fmt.Sprintf("%s/%s", docroot, path)
}
