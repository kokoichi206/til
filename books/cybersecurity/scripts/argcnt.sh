#!/bin/bash -

echo "there are $# arguments"

cnt=0
for ARG
do
    cnt=$(($cnt+1))
    echo arg$cnt: $ARG
done

