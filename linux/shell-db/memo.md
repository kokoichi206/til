## SQL?

- テキストファイル？
  - 優位性
    - 特定のアプリケーションに依存しない
    - 高速で信頼性の高いフィルタコマンドを利用できる
  - しんどいかもなこと
    - データの頻繁な更新が必要な場合
    - データの一部を更新する定式化された巣方がない
    - データ間の不整合が起きてもテキストファイルは感知してくれない
- SQL のメリット
  - トランザクションと排他機構によるデータ破壊防止
  - 標準的言語を用いることによるメンテナンスの継続性向上
  - カラム制約・テーブル制約利用によるスクリプトのロジック簡略化


## SQLite3

``` sql
sqlite3 vote.sqlite3
> CREATE TABLE ballotbox(voter TEXT UNIQUE, cand TEXT);
> .exit

> ALTER TABLE ballotbox RENAME TO bb0;
CREATE TABLE candidaets(cand TEXT UNIQUE);
INSERT INTO candidaets VALUES('赤'), ('青'), ('黄');
INSERT INTO candidaets VALUES('青');
INSERT INTO candidaets VALUES('黄');

CREATE TABLE ballotbox(
  voter TEXT UNIQUE,
  cand TEXT,
  FOREIGN KEY(cand) REFERENCES candidaets(cand)
);

-- 標準ではレコード挿入で制約が無効になってる⁉️!?!?!
PRAGMA foreign_keys = ON;

-- Runtime error: FOREIGN KEY constraint failed (19)
REPLACE INTO ballotbox VALUES('id004', '紫');
```
sudo scp kokoichi@192.168.0.46:/home/kokoichi/ghq/github.com/kokoichi206/nogi-comments/backup_0516 ./



## メモ

### shell

- here document で行頭のタブを取り除くには `<<` を `<<-` にする
  - 有効になるのはハードタブのみ

### そのほか


