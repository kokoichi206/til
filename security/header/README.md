## セキュリティの HTTP レスポンスヘッダ

https://www.youtube.com/watch?v=NRaU_dRvncQ

### Referrer-Policy

- URL に秘密情報が載ってた場合 Referer ヘッダから漏洩する
- 4 種類の Referrer-Policy
  - no-referrer
  - no-referrer-when-downgrade
    - 従来のデフォルト
    - downgrade した時のみ送信しない
  - origin-when-cross-origin
    - 現在のデフォルト
    - 同一オリジンの遷移ではフルの Referrer
    - クロスオリジンでは、オリジンのみ！
  - same-origin
- この辺は**遷移元となってるページの response の header** にポリシーを設定して挙動を変える
- **通常はデフォルトでよい**

### Strict-Transport-Security (HSTS)

- `Strict-Transport-Security: max-age=3153600; includeSubDomains`
- 対策されるもの
  - 中間間攻撃の脅威
    - HTTP に誘導され、盗聴・改竄
  - クッキーの SameSite=Strict の回避
- [偽Wi-Fiアクセスポイントで本当にパスワードは盗聴できるか試してみた](https://www.youtube.com/watch?v=k0xBCjWPqcU&ab_channel=%E5%BE%B3%E4%B8%B8%E6%B5%A9%E3%81%AE%E3%82%A6%E3%82%A7%E3%83%96%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3%E8%AC%9B%E5%BA%A7)
- [常時SSLでもCookieの改ざんはできるワケ](https://www.eg-secure.co.jp/tokumaru/youtube/35)
- **ぜひ設定すべき**

### X-Content-Type-Options

- Content-Type を無視する挙動は**モダンブラウザでも残っている**
  - [main.go](./main.go)
- **設定すると少し安全**

### X-Frame-Options

- クリックジャッキングの対策として！
  - Web Intent とか
- 必要性は薄くなってはいる
- ブラウザの努力により、クリックジャッキング自体は絶滅危惧種に
- サードパーティークッキーが無効になっているとさらに効かない
  - サードパーティークッキーを段階的に廃止する
- **サードパーティークッキー**
  - 伝統的な仕様
    - サイト A でセットされた Cookie が、他のサイトの iframe 等の中でも同じ Cookie として扱われる
  - 無効な場合
    - 元はトラッキング防止の対策だが、セキュリティを高めることもにも効果がある
    - iframe や XHR/Fetch を使った XSS, CSRF 等の緩和策として効果がある
- **ぜひ設定すべき**

### X-XSS-Protection

- XSS Fiter (XSS Auditor)
  - 反射型 XSS を防ぐための、ブラウザ側セキュリティ機能
- X-XSS-Protection
- **X-XSS-Protection は廃止されている**
  - 現在のブラウザでは！
  - Firefox では一度も実装していない
- **CSP: Content-Security-Policy を使いましょう**
- ブラウザ上意味がない
