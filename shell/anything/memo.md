``` sh
# 画面を F で埋め尽くすだけ。面白い。
C=$(tput cols);L=$(tput lines);while :;do x=$(($RANDOM%$C));y=$(($RANDOM%$L));printf "\033[${y};${x}fF";done
```
