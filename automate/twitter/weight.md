## unix timeで時間を表示
date +%s
## unix time から日付への変換方法
date --date "@1305730800"
echo 1305730800 | awk '{print strftime("%c",$1)}'
