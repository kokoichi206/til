cgi 関係の設定

```sh
$ sudo vim /etc/apache2/conf-available/serve-cgi-bin.conf

 1 <IfModule mod_alias.c>                                                            
  2 ▸---<IfModule mod_cgi.c>
  3 ▸---▸---Define ENABLE_USR_LIB_CGI_BIN
  4 ▸---</IfModule>
  5 
  6 ▸---<IfModule mod_cgid.c>
  7 ▸---▸---Define ENABLE_USR_LIB_CGI_BIN
  8 ▸---</IfModule>
  9 
 10 ▸---<IfDefine ENABLE_USR_LIB_CGI_BIN>
 11 ▸---▸---# ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
 12 ▸---▸---ScriptAlias /api/v1/ /usr/lib/cgi-bin/server.cgi/
 13 ▸---▸---<Directory "/usr/lib/cgi-bin">
 14 ▸---▸---▸---AllowOverride None
 15 ▸---▸---▸---Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
 16             AddHandler cgi-script .cgi .pl .py .rb
 17 ▸---▸---▸---Require all granted
 18 ▸---▸---</Directory>
 19 ▸---</IfDefine>
 20 </IfModule>
 21 <Directory "/var/www/html/cgi-enabled">
 22     Options +ExecCGI
 23     AddHandler cgi-script .cgi .pl .py .rb
 24 </Directory>
```


```sh
ubuntu@ubuntu:~/work/go/web$ go build -ldflags "-s -w" -o server.cgi server.go
ubuntu@ubuntu:~/work/go/web$ sudo mv server.cgi /usr/lib/cgi-bin/
ubuntu@ubuntu:~/work/go/web$ sudo systemctl restart apache2
```
