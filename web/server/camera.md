
```sh
# usb 接続状況を確認
$ lsusb

$ ls /dev/video*
```


### mjpg-stream
```sh
sudo apt-get install -y subversion libjpeg-dev imagemagick

```

### port
```
http://192.168.3.7:8888/

```

### リダイレクトさせる
- [proxy の有効化](https://qiita.com/niwasawa/items/bb4ba35b6b318bb4e278)
- [redirect example](https://solmaz.io/2017/01/13/apache-redirect-path-to-port/)

```sh
# 必要な設定を有効化する
$ sudo a2enmod proxy_http
Considering dependency proxy for proxy_http:
Enabling module proxy.
Enabling module proxy_http.
To activate the new configuration, you need to run:
  systemctl restart apache2
```

```sh
```

