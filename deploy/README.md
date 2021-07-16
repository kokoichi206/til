# deplpy
- Github Actionsを使ってCIしたい！
  - vueのbuild
  - 静的ファイルを然るべき場所に配置してgithub pagesに公開

## ハマったところ
- cdコマンドは使えるが、毎回WorkingDir（TOP）に戻るらしい

## npm ciでこける
- packege-lock.jsonがなかったっぽい！
- [インストールする](https://codehero.jp/node.js/46653833/is-there-a-way-to-force-npm-to-generate-package-lock-json)
  - `npm install --package-lock`
