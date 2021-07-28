#!/bin/bash
#
# Description:
# Count lines every n seconds
#
# Usage: ./tailcount.sh [filename]
#   filename: passed to looper.sh
#

# cleanup - the other processes on exit
function cleanup ()
{
    [[ -n $LOPID ]] && kill $LOPID
}

trap cleanup EXIT

bash looper.sh $1 &
LOPID=$!
# give it a chance to start up
sleep 3

while true
do
    kill -SIGUSR1 $LOPID
    sleep 5
done >&2
