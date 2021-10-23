## DB アクセスがうまくいかない
- golang での db を用いた API, ok
- golang を cgi に変えて、apache の上で動かす、ok

この状況で、db を用いた API を、cgi に変えて、apache の上で動かすと、失敗した

```sh
% curl "https://kokoichi0206.mydns.jp/cgi-bin/server.cgi/members?gn=sakurazaka"
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>500 Internal Server Error</title>
</head><body>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error or
misconfiguration and was unable to complete
your request.</p>
<p>Please contact the server administrator at 
 webmaster@localhost to inform them of the time this error occurred,
 and the actions you performed just before this error.</p>
<p>More information about this error may be available
in the server error log.</p>
</body></html>
```

apache log

```sh
$ cat /var/log/apache2/error.log
[Sun Oct 17 14:39:05.060066 2021] [cgid:error] [pid 1523073] 
[client 2400:2410:2d83:9500:615e:c428:7e1d:184e:62714]
malformed header from script 'server.cgi': Bad header: &{0 {host=localhost port=5432
```

関係ありそうな箇所としては、db コネクションをしている部分、

```go
UserInfo   = "host=localhost port=5432 user=ubuntu password=" + DbPass + " dbname=" + DbName + " sslmode=disable"
func DbInit() (*sql.DB, error) {
	con, err := Connect()
	Ctx = context.Background()
	return con, err
}
```

header がどうこう言ってたので、以下のように header をつけてあげたら違うエラー内容になった

```go
UserInfo   = "Content-type:text/plain\n\n" + "host=localhos...
```

apache 

```sh
[Sun Oct 17 14:44:02.326470 2021] [http:error] [pid 1524572] 
[client 2400:2410:2d83:9500:615e:c428:7e1d:184e:64020] AH02429: Response header name 
'&{0 {Content-type' contains invalid characters, aborting request
```

うーん、db アクセスだから、ヘッダーとかは必要ないと思うねんけどなぁ....



### 他に試してみたこと
- `/var/lib/pgsql/data/pg_hba.conf`ファイルで、全てのクライアントに対し、対象 DB への接続を許可した
  - apache の仕組みによっては、接続もとが変わってるかもと思ったので
- firewall で、5432 のポートを解放


## 各種ファイルの中身どんなのかまとめ
```sh
$ sudo vim /etc/apache2/apache2.conf

<Directory /var/www/html>
▸---AllowOverride None
▸---Require all granted
#    AliasMatch ^/api/(.*) https://www.google.com/search?q=$1
</Directory>
```

