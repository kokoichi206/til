# Unixテキスト処理〜連載第一回目

## コマンド例
```bash
# 空行を削除
$ grep -v '^$' ex.txt
$ sed '/^$/d' ex.txt
$ awk 'NF!=0' ex.txt
# 逆の列から読む、catの逆！！！
$ tac ex.txt
# 行の左右反転
$ rev ex.txt
```

## 回文チェック
遅い方法
```bash
while read line; do if [ "${line}" = "$(echo ${line} | rev)" ]; then echo $line; fi; done < examination.txt
```

良い方法
```bash
paste examination.txt <(rev examination.txt) | awk '$1==$2{print $1}'
```
