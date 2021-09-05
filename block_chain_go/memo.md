## メモ
コードを整形してくれる

```sh
gofmt -w block/goblockchain.go
```

### 検索履歴
- [command-line-arguments ~ undefined](https://qiita.com/kosukeKK/items/abb208fd0bbd3744ddfb)
  - `go run main.go blockchain_server.go -port 5001`


### API

#### /amount
block chain address をパラメータとして渡し、そのアカウントの持つ総コイン量を求める

http://localhost:5000/amount?blockchain_address=1DSTFJMa4YA4nh128iLcWNba3QcZSNBCzZ
