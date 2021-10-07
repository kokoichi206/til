## sec 9 インターネットと通信

### html
```sh
$ man sed
-n, --quiet, --silent
    suppress automatic printing of pattern space

$ cat stracture.html | grep -o '<title>.*</title>'
$ cat stracture.html | sed -n '/<ul>/, /<\/ul>/p' | sed '1d; $d'
```

### 名前解決
```sh
# ここをいじると変わる
$ cat /etc/hosts
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
```

### dig
```sh
$ dig google.com

; <<>> DiG 9.16.1-Ubuntu <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 31243
...
```

```sh
$ dig localhost
...
localhost.              0       IN      A       127.0.0.1
...
```

### nc
nc — arbitrary TCP and UDP connections and listens

### パケットを使った OS の推定
```sh
# grep -m
## -m NUM, --max-count=NUM
##    Stop reading a file after NUM matching lines.
## -P, --perl-regexp
$ ping -4 gihyo.jp | grep -m 1 -oP 'ttl=\K\d+'
58

$ sudo traceroute -I google.com
traceroute to google.com (142.250.196.142), 64 hops max
  1   192.168.3.1  0.715ms  0.636ms  0.656ms 
  2   221.110.222.214  5.887ms  5.823ms  10.893ms 
  ...
  8   142.250.196.142  6.824ms  6.830ms  6.500ms 
```



## 小ネタ

