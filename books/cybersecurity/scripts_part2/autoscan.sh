#!/bin/bash -
#
# Description:
# Automatically performs a port scan (using scan.sh)
# compares output to previous results, and emails user
# Assumes that scan.sh is in the current directory.
#
# Usage: ./autoscan.sh
#

./scan.sh < hostlist

FILELIST=$(ls scan_* | tail -2)
FILES=( $FILELIST )

TMPFILE=$(tempfile)

./fd2.sh ${FILES[0]} ${FILES[1]} > $TMPFILE

if [[ -s $TMPFILE ]] # non-empty
then
    echo "mailing today's port differences to $USER"
    mail -s "today's port difference" $USER < $TMPFILE
fi
# clean up
rm -r $TMPFILE
