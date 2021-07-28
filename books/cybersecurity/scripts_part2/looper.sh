#!/bin/bash -
#
# Description:
# Count the lines in a file being tailed -f
#
# Report the count interval on every SIGUSR1
#
# Usage: ./looper.sh [filename]
#   filename of file to be tailed, default: log.file
#

function interval ()
{
    echo $(date '+%y%m%d %H%M%S') $cnt
    cnt=0
}

declare -i cnt=0
trap interval SIGUSR1

shopt -s lastpipe

tail -f --pid=$$ ${1:-log.file} 2> /dev/null | while read aline
do
    let cnt++
done
