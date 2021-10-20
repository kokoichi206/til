cgi 関係の設定

```sh
$ sudo vim /etc/apache2/conf-available/serve-cgi-bin.conf
```


```sh
ubuntu@ubuntu:~/work/go/web$ go build -ldflags "-s -w" -o server.cgi server.go
ubuntu@ubuntu:~/work/go/web$ sudo mv server.cgi /usr/lib/cgi-bin/
ubuntu@ubuntu:~/work/go/web$ sudo systemctl restart apache2
```
