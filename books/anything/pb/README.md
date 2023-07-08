## docs

``` sh
go install github.com/pseudomuto/protoc-gen-doc/cmd/protoc-gen-doc@latest

protoc --doc_out=./doc --doc_opt=html,index.html *.proto

protoc --doc_out=./doc --doc_opt=markdown,index.md proto/*.proto
```

## Buf CLI

``` sh
# https://buf.build/docs/installation/
brew install bufbuild/buf/buf

buf --version

# インデントや空行のフォーマットを整える！
buf format --write
```

``` sh
buf mod initbuf mod update

buf format -w
```

- コード生成
- format, lint
- 破壊的変更の検出


## Links

- https://github.com/pseudomuto/protoc-gen-doc/
- [Protocol Buffers DON'TS](https://protobuf.dev/programming-guides/dos-donts/)
- https://cloud.google.com/apis/design/resources?hl=ja
- VSCode extension: for buf
  - https://github.com/bufbuild/vscode-buf
- Detect Breaking changes in ci
  - https://github.com/bufbuild/buf-breaking-action
  - https://mionskowski.pl/posts/ci-pipeline-for-protobuf/
- https://github.com/bufbuild/buf
