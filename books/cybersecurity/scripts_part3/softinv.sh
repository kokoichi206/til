#!/bin/bash -
#
# Description:
# list the software installed on a system
# for later aggregation and analysis
#
# Usage: ./softinv.sh [filename]
# output is written to $1 or <hostname>_softinv.txt
#

# set the output filename
OUTFN="${1:-${HOSTNAME}_softinv.txt}"

# which command to run depends on the OS and what's there
OSbase=win
type -t rpm &> /dev/null
(( $? == 0 )) && OSbase=rpm
type -t dpkg &> /dev/null
(( $? == 0 )) && OSbase=deb
type -t apk &> /dev/null
(( $? == 0 )) && OSbase=apt

case ${OSbase} in
    win)
        INVCMD="wmic product get name,version //format:csv"
        ;;
    rpm)
        INVCMD="rpm -qa"
        ;;
    deb)
        INVCMD="dpkg -l"
        ;;
    apt)
        INVCMD="apt list --installed"
        ;;
    *)
        echo "error: OSbase=${OSbase}"
        exit -1
        ;;
esac

#
# run the inventory
#
[[ $1 == "-" ]] && $INVCMD && exit 0
$INVCMD 2>/dev/null > $OUTFN
