# TDD?
- Test Driven Development
- [参考にした本（テスト駆動開発）](https://www.amazon.co.jp/%E3%83%86%E3%82%B9%E3%83%88%E9%A7%86%E5%8B%95%E9%96%8B%E7%99%BA-Kent-Beck/dp/4274217884)

## テスト駆動開発
- 動作するきれいなコード

### シンプルな２つのルール
- 自動化されたテストが失敗した時のみ、新しいコードを書く
- 重複を除去する

### TDDが機械的に示せない２大トピック
- セキュリティ
- 並行性


## Javaの実行環境構築
```sh
$ brew install java
$ java --version
# なんかシンボリックリンクを貼る必要がある
$ sudo ln -sfn $(brew --prefix)/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
$ java --version
```

