#!/bin/bash -
#
# Description:
# Creates a rolling horizontal bar chart of live data
#
# Usage:
# <output from other script or program> | bash livebar.sh
#

function pr_bar ()
{
    local raw maxraw scaled
    raw=$1
    maxraw=$2
    ((scaled=(maxbar*raw)/maxraw))
    ((scaled == 0)) && scaled=1     # min size guarantee
    for((i=0; i<scaled; i++)); do printf '#'; done
    printf '\n'
}   # pr_bar

max_bar=60      # largest no. of chars in a bar
MAX=60
while read dayst timst qty
do
    if (( qty > MAX ))
    then
        let MAX=$qty+$qty/4     # allow some room
        echo "          **** rescaling: MAX=$MAX"
    fi
    printf '%6.6s %6.6s %4d:' $dayst $timst $qty
    pr_bar $qty $MAX
done
