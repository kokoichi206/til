#!/bin/bash -
#
# Description:
# Use ping to monitor host availability
#
# Usage:
# pingmonitor.sh <file> <seconds>
#   <file> File containing a list of hosts
#   <seconds> Number of seconds between pings
#

while true
do
    clear
    echo 'Cybersecurity Ops System Monitor'
    echo 'Status: Scanning ...'
    echo '-------------------------'
    while read -r ipadd
    do
        ipadd=$(echo "$ipadd" | sed 's/\r//')
        echo "$ipadd"
        ping -c 1 "$ipadd" | egrep '(Destination host unreachable|100%)' &> /dev/null
        if(( "$?" == 0 ))
        then
            echo "NOT FOUND"
            tput setaf 1
            echo "Host $ipadd not found - $(date)" | tee -a monitorlog.txt
            tput setaf 7
        fi
        echo "IIII"
    done < "$1"

    echo ""
    echo "Done."

    for ((i="$2"; i>0; i--))
    do
        tput cup 1 0
        echo "Status: Next scan in $i seconds"
        sleep 1
    done
done
