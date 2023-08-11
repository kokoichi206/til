#!/bin/bash

expect -c "
    # 5 秒でタイムアウトにする。
    set timeout 15
    # 実行したいコマンド。
    spawn systemctl restart sakamichi-api-bff.service

    # ターミナル上に現れることが期待される文言。
    expect \"Password:\"
    # 打ち込みたい内容。パスワードの例。
    send \"root_pass\"
    send \"\n\"

    expect \"$:\"
    exit 0
"
