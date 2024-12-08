#!/usr/bin/env bash
set -euo pipefail

URI="http://localhost/"

# 初期化。
true > /var/log/nginx/access.log

nginx -s reopen

# ab -c 1 -t 30 "${URI}"
# ab -c 2 -t 30 "${URI}"

# ab -c 1 -t 15 "${URI}"
# ab -c 2 -t 15 "${URI}"
ab -c 8 -t 15 "${URI}"


mv /var/log/nginx/access.log "/var/log/nginx/access.log.$(date "+%Y%m%d%H%M%S")"
