#!/usr/bin/env bash
set -euo pipefail

# ==================== reset ====================
true > /var/log/nginx/access.log
nginx -s reopen

MYSQL_PWD='isuconp' mysql -u isuconp -e "SET GLOBAL slow_query_log = 1;" isuconp
DATETIME=$(date "+%Y%m%d-%H%M%S")
MYSQL_PWD='isuconp' mysql -u isuconp -e "SET GLOBAL slow_query_log_file = '/var/log/mysql/mysql-slow-$DATETIME.log';"
MYSQL_PWD='isuconp' mysql -u isuconp -e "SET GLOBAL long_query_time = 0;" isuconp
# ==================== reset ====================

# 諸々の試験を行う。。。
k6 run integrated.js

# slow query log を閉じる。
MYSQL_PWD='isuconp' mysql -u isuconp -e "SET GLOBAL slow_query_log = 0;" isuconp

cp /var/log/nginx/access.log "/var/log/nginx/access.log.$DATETIME"
nginx -s reopen


# Profile
# Rank Query ID                      Response time Calls R/Call V/M   Item
# ==== ============================= ============= ===== ====== ===== ====
#    1 0xA047A0D0BA167343E5B36786...  1.0537 45.0% 11556 0.0001  0.00 SELECT users
#    2 0xDA556F9115773A1A99AA0165...  0.8320 35.5% 11564 0.0001  0.00 ADMIN PREPARE
#    3 0x4858CF4D8CAA743E839C127C...  0.2546 10.9%     8 0.0318  0.00 SELECT posts
#    4 0x5C29F616FBA5526D7150C784...  0.1400  6.0%     8 0.0175  0.00 SELECT users
# MISC 0xMISC                         0.0633  2.7% 11583 0.0000   0.0 <11 ITEMS>
echo run: sudo pt-query-digest /var/log/mysql/mysql-slow-$DATETIME.log

# +-------+--------+-------------+-------+-------+-------+--------+
# | COUNT | METHOD |     URI     |  MIN  |  AVG  |  MAX  |  SUM   |
# +-------+--------+-------------+-------+-------+-------+--------+
# | 22555 | GET    | /login      | 0.000 | 0.001 | 0.100 | 16.554 |
# | 11548 | POST   | /           | 0.000 | 0.001 | 0.093 | 10.667 |
# | 11556 | POST   | /login      | 0.000 | 0.001 | 0.152 | 10.612 |
# | 8     | GET    | /           | 0.676 | 0.763 | 0.845 | 6.102  |
# | 8     | POST   | /comment    | 0.000 | 0.004 | 0.030 | 0.035  |
# | 1     | GET    | /initialize | 0.008 | 0.008 | 0.008 | 0.008  |
# +-------+--------+-------------+-------+-------+-------+--------+
echo run: alp json --sort sum -r -m "/posts/[0-9]+,/@\w+" -o count,method,uri,min,avg,max,sum \< /var/log/nginx/access.log.$DATETIME
