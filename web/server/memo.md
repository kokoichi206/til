## Apache2

```
go build -ldflags "-s -w" -o server.cgi server.go

$ sudo systemctl restart apache2
```

cgi ファイルの置き場所。 - /usr/lib/cgi-bin

それはここに書いてある
$ cat /etc/apache2/conf-enabled/serve-cgi-bin.conf 


[go から cgi にして配信するまで](https://tech-blog.s-yoshiki.com/entry/188)
[apache2 ubuntu の設定方法](https://www.server-world.info/query?os=Ubuntu_20.04&p=httpd&f=5)


## PostgreSql
[ubuntu にローカルサーバーで DB を立てる](https://www.server-world.info/query?os=Ubuntu_20.04&p=postgresql12&f=1)


```sh
$ sudo apt -y install postgresql-12
$ ls /etc/postgresql/12/main/
conf.d	environment  pg_ctl.conf  pg_hba.conf  pg_ident.conf  postgresql.conf  start.conf

# 認証方式を確認
$ sudo grep -v -E "^#ø^$" /etc/postgresql/12/main/pg_hba.conf
local   all             postgres                                peer
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
```

```sh
$ su - postgres

# root になってから使う
ubuntu@ubuntu:/usr/lib/cgi-bin$ sudo su -
root@ubuntu:~# su - postgres

# PostgreSQL 管理ユーザーで PostgreSQL ユーザーとデータベース追加
root@dlp:~# su - postgres
postgres@dlp:~$ createuser ubuntu
postgres@dlp:~$ createdb testdb -O ubuntu

# 上のように ubuntu で登録しておくと、ubuntu でその db が使える
ubuntu@ubuntu:~/work$ psql sakamichi
psql (12.8 (Ubuntu 12.8-0ubuntu0.20.04.1))
Type "help" for help.

sakamichi=> 
```

ここからは好きなように遊んだら良い

```sh
# テストテーブルを作成
testdb=> create table test_table (no int, name text); 
CREATE TABLE

# テーブル一覧を表示
testdb=> \dt 
          List of relations
 Schema |    Name    | Type  | Owner
--------+------------+-------+--------
 public | test_table | table | ubuntu
(1 row)

# テストテーブルにテストデータを挿入
testdb=> insert into test_table (no,name) values (01,'Ubuntu'); 
INSERT 0 1
```

### db のパスワード設定
任意の PostgreSQL ユーザーでパスワード認証でデータベースへ接続するために、パスワードをセットしておきます。

```sh
# 自身が所有するデータベースに接続
ubuntu@dlp:~$ psql -d testdb
psql (12.4 (Ubuntu 12.4-0ubuntu0.20.04.1))
Type "help" for help.

# 自身のパスワードを設定/変更
testdb=> \password
Enter new password:
Enter it again:
testdb=> \q

# PostgreSQL 管理ユーザーから任意のユーザーのパスワードを設定/変更する場合は以下
postgres@dlp:~$ psql -c "alter user ubuntu with password 'password';"
ALTER ROLE
```

### サーバーとして立ち上げる？
```sh
sudo service postgresql restart

```


