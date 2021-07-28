#!/bin/bash -
#
# Usage: ./useragents.sh < <inputfile>
#   <inputfile> Apache access log
#

# mismatch - search through the array of known names
#   return 1 (false) if it finds a match
#   return 0 (true) if there is no match
function mismatch ()
{
    local -i i
    for ((i=0; i<$KNSIZE; i++))
    do
        [[ "$1" =~ .*${KNOWN[$i]}.* ]] && return 1
    done
    return 0
}

# read up the known ones
readarray -t KNOWN < "useragents.txt"
KNSIZE=${#KNOWN[@]}

does_use_file=false
if [ "$1" == "-f" ]
then
    does_use_file=true
    FILENAME=$2
    if [ ! $FILENAME ]
    then
        printf "usage:\n useragents.sh -f <FILENAME>\n"
        exit
    fi
fi

# preprocess logfile (stdin) to pick out ipaddr and user agent
awk -F'"' '{print $1, $6}' | \
while read ipaddr dash1 dash2 dtstamp delta useragent
do
    if mismatch "$useragent"
    then
        if [ does_use_file ]
        then
            echo "anomaly: $ipaddr $useragent" >> "./$FILENAME"
        else
            echo "anomaly: $ipaddr $useragent"
        fi
    fi
done
