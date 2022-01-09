#!/bin/bash -
#
# Description:
# Count the number of instances of  an item
#
# Usage:
# countem.sh < inputfile
#

declare -A cnt
while read id xtra
do
    let cnt[$id]++
done
for id in "${!cnt[@]}"
do
    printf '%d %s\n' "${cnt[$id]}" "$id"
done
