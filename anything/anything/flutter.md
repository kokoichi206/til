## マルチモジュール

https://www.youtube.com/watch?v=xh2E5Tg2r3A&ab_channel=FlutterKaigi

マルチモジュールのメリット

- 影響範囲が限定的になる
  - ライブラリが死んだ時も、特定箇所のみ見れば良くなったりする
  - 外部公開しているところのみ重点的にレビューしたら良くなる
  - Need Not To Know をソースコードレベルで行える
- ドメイン層は積極的に分割する
- 画面単位の分割
  - 画面遷移を伴う部分は、基本分割対象とする
- インフラ層の分割
  - プラグイン（ネイティブコード）を必要とする処理はモジュールを分ける！
  - プラグインはマルチプラットフォームでは、常にリスクと隣り合わせ！
  - Web では File System が使えないなど、プラットフォーム固有の知識も、適切な分割のために必要

完璧にするコストと、完璧でないリスクを天秤にかける！！

annotation で internal を絞ることができるらしい。  
CI の Analyzer を上手く使う！

`flutter analyze`

Analyzer は最新に保つ！

意図しない直接 import を防ぐためにも、  
`depend_on_referenced_packages` は有効にしておく！

CI  
並列化しすぎると、オーバーヘッドの時間（pub get 等）が増え、コストが増大する。

未解決？  
多言語対応ファイルをどのように分割するか（公式に記載なし）