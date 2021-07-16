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

## ciを用いてdeploy
- [gh-pages](https://github.com/peaceiris/actions-gh-pages)
- [githubのsetting方法](https://github.com/peaceiris/actions-gh-pages#%EF%B8%8F-first-deployment-with-github_token)
  - Sourceは、`Branch:gh-pages`の`folder: /(root)`にする

## deployできたけど画面が真っ白
- `vue.config.js`のファイルを作り、以下を記述

```
module.exports = {
    outputDir: './dist/',
    publicPath: './'
}
```
