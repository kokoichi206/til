# Mediator
相手は相談役１人だけ

## Mediator パターン
**メンバーはみんな相談役だけに報告し、メンバーへの指示は相談役だけからくる**ようにする。そして、メンバー同士が状況を探りあったり、指示しあったりすることはない。

Mediator パターンでは、**「相談役」は mediator（調停者）、「各メンバー」は colleague（同僚）と呼ぶ**。

## サンプルプログラム
「名前とパスワードを入力するログインダイアログ」という GUI アプリケーションを作る。

GUI において、それぞれのオブジェクトが互いに関係し合っているため、お互いがお互いをコントロールするような状況に陥ってしまう。

上記のような、**多数のオブジェクトの間の調整を行わなければならない時こそ、Mediator パターンの出番**。個々のオブジェクトが互いに通信し合うのではなく、「頼りになる相談役」を置き、その相談役とだけ通信することとする。そして、**表示のコントロールのロジックは、相談役の中にだけ記述する**。


## ヒント

**アプリケーションへの依存性が高いということは、再利用性が低い**ということ
