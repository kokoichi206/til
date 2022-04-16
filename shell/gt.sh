#!/bin/bash

msg="hoge"

count=0
while [ "$count" -lt "${#msg}" ]; do
    echo "${msg:count:1}"
    echo "$count"
    ((count++))
done
