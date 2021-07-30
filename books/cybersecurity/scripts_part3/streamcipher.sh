#!/bin/bash -
#
# Description:
# A lightweight implementation of a stream cipher
# Pedagogical - not recommended for serious use
#
# Usage:
# streamcipher.sh [-d] <key> < inputfile
#   -d Decrypt mode
#   <key> Numeric key
#

source ./askey.sh

#
# Ncrypt - Encrypt - reads in characters
#       outputs 2digit hex #s
#
function Ncrypt ()
{
    TXT="$1"
    for((i=0; i<${#TXT}; i++))
    do
        CHAR="${TXT:i:1}"
        RAW=$(asnum "$CHAR")    # " " needed for space (32)
        NUM=${RANDOM}
        COD=$(( RAW ^ ( NUM & 0x7F )))
        printf "%02X" "$COD"
    done
    echo
}

#
# Dcrypt - DECRYPT - reads in a 2digit hex #s
#       outputs characters
#
function Decrypt ()
{
    TXT="$1"
    for((i=0; i<${#TXT}; i=i+2))
    do
        CHAR="0x${TXT:i:2}"
        RAW=$(( $CHAR ))
        NUM=${RANDOM}
        COD=$(( RAW ^ ( NUM & 0x7F )))
        aschar "$COD"
    done
    echo
}

if [[ -n $1 && $1 == "-d" ]]
then
    DECRYPT="YES"
    shift
fi

KEY=${1:-1776}
RANDOM="${KEY}"
while read -r
do
    if [[ -z $DECRYPT ]]
    then
        Ncrypt "$REPLY"
    else
        Dcrypt "$REPLY"
    fi
done
