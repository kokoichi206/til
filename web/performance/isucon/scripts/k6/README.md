## k6 scripts

### install

- https://grafana.com/docs/k6/latest/set-up/install-k6/

``` sh
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

### run

``` sh
# Flags:
#   -u, --vus int                             number of virtual users (default 1)
k6 run --vus 1 --duration 30s ab.js

...
http_reqs......................: 746   24.854531/s
```

ab.js


``` sh
k6 run --vus 1 initialize.js

k6 run integrated.js
```

## memo

- k6 は redirect を勝手に解釈する
  - check などでの確認は redirect 後の値になる
