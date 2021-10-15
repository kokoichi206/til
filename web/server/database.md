## 注意すること

### 生のクエリ
insert 時の VALUES は、シングルクォーテーションで囲むこと！（× ダブルクォーテーション）

```sql
sakamichi=> SELECT song_id, group_id, single, title, first_row_num, second_row_num, third_row_num
sakamichi->     FROM songs INNER JOIN formations
sakamichi->         ON songs.formation_id = formations.formation_id;

 song_id | group_id | single |               title                | first_row_num | second_row_num | third_row_num 
---------+----------+--------+------------------------------------+---------------+----------------+---------------
       1 |        2 | 1st    | キュン                             |             5 |              6 |             9
       2 |        2 | 2nd    | ドレミソラシド                     |             5 |              6 |             8
       3 |        2 | 3rd    | こんなに好きになっちゃっていいの？ |             3 |              6 |             9
       4 |        2 | 4th    | ソンナコトナイヨ                   |             5 |              6 |             7
       6 |        2 | 5th    | 膨大な夢に押し潰されて             |             5 |              7 |            10
       5 |        2 | 5th    | 君しか勝たん                       |             5 |              7 |            10
      61 |        2 | 5th    | 声の足跡                           |             6 |              7 |             9
      63 |        2 | 5th    | 世界にはThank you！が溢れている    |             3 |              6 |             0
      62 |        2 | 5th    | どうする？どうする？どうする？     |             3 |              6 |             0
      71 |        2 | 6th    | 酸っぱい自己嫌悪                   |             4 |              0 |             0
      64 |        2 | 5th    | Right？                            |             4 |              0 |             0
      68 |        2 | 6th    | 何度でも何度でも                   |             5 |              7 |             9
      67 |        2 | 6th    | アディショナルタイム               |             5 |              7 |             9
      66 |        2 | 6th    | 思いがけないダブルレインボー       |             5 |              7 |             9
      65 |        2 | 6th    | ってか                             |             5 |              7 |             9
      69 |        2 | 6th    | 夢は何歳まで？                     |             2 |              0 |             0
      70 |        2 | 6th    | あくびLetter                       |             3 |              0 |             0

```

```sql
 position_id | position |               title                |  single   |   name_ja   
-------------+----------+------------------------------------+-----------+-------------
          18 | 003      | キュン                             | 1st       | 小坂 菜緒
          37 | 003      | ドレミソラシド                     | 2nd       | 小坂 菜緒
          56 | 002      | こんなに好きになっちゃっていいの？ | 3rd       | 小坂 菜緒
          73 | 003      | ソンナコトナイヨ                   | 4th       | 小坂 菜緒
          95 | 003      | 君しか勝たん                       | 5th       | 加藤 史帆
         117 | 003      | 膨大な夢に押し潰されて             | 5th       | 加藤 史帆
         182 | 003      | ってか                             | 6th       | 金村 美玖
         203 | 003      | 思いがけないダブルレインボー       | 6th       | 金村 美玖
         224 | 003      | アディショナルタイム               | 6th       | 金村 美玖
         245 | 003      | 何度でも何度でも                   | 6th       | 上村 ひなの
         276 | 003      | アザトカワイイ                     | 1st Album | 佐々木 美玲
```

```go
_, execErr := DB.Exec(`CREATE TABLE IF NOT EXISTS test_user (
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(10))`)
if execErr != nil {
	fmt.Println("Pien, could not create db")
}
```
