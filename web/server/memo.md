```
go build -ldflags "-s -w" -o server.cgi server.go

$ sudo systemctl restart apache2
```

cgi ファイルの置き場所。 - /usr/lib/cgi-bin

それはここに書いてある
$ cat /etc/apache2/conf-enabled/serve-cgi-bin.conf 


[go から cgi にして配信するまで](https://tech-blog.s-yoshiki.com/entry/188)
[apache2 ubuntu の設定方法](https://www.server-world.info/query?os=Ubuntu_20.04&p=httpd&f=5)


