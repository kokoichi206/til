#!/bin/bash -
#
# Description:
# Compares two port scans to find changes
# MAJOR ASSUMPTION: both files have the same # of lines,
# each line with the same host address
# though with possibly different listed ports
#
# Usage: ./fd2.sh <file1> <file2>
#

# look for "$LOOKFOR" in the list of args to this function
# returns true (0) if it is not in the list
function NotInList ()
{
    for port in "$@"
    do
        if [[ $port == $LOOKFOR ]]
        then
            return 1
        fi
    done
    return 0
}

while true
do
    read aline <&4 || break     # at EOF
    read bline <&5 || break     # at EOF, for symmetry

    # if [[ $aline == $bline ]]; then continue; fi
    [[ $aline == $bline ]] && continue;

    # there's a difference, so we
    # subdivide into host and ports
    HOSTA=${aline%% *}
    PORTSA=( ${aline#* } )

    HOSTB=${bline%% *}
    PORTSB=( ${bline#* } )

    echo $HOSTA         # identify the host which changed

    for porta in ${PORTSA[@]}
    do
        LOOKFOR=$porta NotInList ${PORTSB[@]} && echo "  closed: $porta"
    done

    for portb in ${PORTSB[@]}
    do
        LOOKFOR=$portb NotInList ${PORTSA[@]} && echo "     new: $portb"
    done

done 4< ${1:-day1.data} 5< ${2:-day2.data}
# day1.data and day2.data are default names to make it easier to test

