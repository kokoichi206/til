## [LOCUST](https://locust.io/)

locust はイナゴ

### [Installation](https://docs.locust.io/en/stable/installation.html)

```sh
pip3 install locust

locust -V
locust 2.12.2 from ... (python 3.10.0)
```

### Run

```sh
# locustfile.py というファイル名で用意し、1 コマンド打つだけ
locust
```

ローカルサーバーへアクセス
http://localhost:8089/#

Spawn rate
1 秒あたりに増加するユーザーの数。
