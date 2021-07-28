#!/bin/bash
#
# Usage: ./histogram.sh
#   input format: label value
#

function pr_bar ()
{
    local -i i raw maxraw scaled
    raw=$1
    maxraw=$2
    ((scaled=(MAXBAR*raw)/maxraw))
    # min size guarantee
    ((raw > 0 && scaled == 0)) && scaled=1

    for((i=0; i<scaled; i++)); do printf '#'; done
    printf '\t%d\n' "$raw"
}

#
# "main"
#
declare -A RA
declare -i MAXBAR max
max=0
MAXBAR=50   # how large the largest bar should be

if [ "$1" = "-s" ]
then
    MAXBAR=$2
fi

while read label val
do
    let RA[$label]=$val
    # keep the largest value; for scaling
    (( val > max )) && max=$val
done

# scale and print it
for label in "${!RA[@]}"
do
    printf '%-20.20s ' "$label"
    pr_bar ${RA[$label]} $max
done
