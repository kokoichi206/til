## はじめに

デザインパターンは、ライブラリそのものではない。
しかし、Java の標準的なクラスライブラリの中には、いくつかのデザインパターンが生かされているクラスがある。

- java.util.Iterator
- java.util.Calendar#getInstance
- java.security.SecureRandom#getInstance
- java.awt.Component

### プログラムを完成品として見ないこと

デザインパターンの目標の1つは、プログラムを再利用可能にすること。つまり、どうやってプログラムを「部品」として再利用するかを考えている。よって、今後「機能を拡張していくもの」としてみるようにする

- どのような機能が拡張される可能性があるか？
- その機能拡張を行うときに修正が必要になるのはどのクラスか？
- 修正が不要なのはどのクラスか？

このような観点でデザインパターンを見ると良い。

## Iterator パターン
- 変数 i の働きを抽象化したもの。
- 何かがたくさん集まっているときに、ソレを順番に指し示していき、全体をスキャンしていく処理を行うもの。

