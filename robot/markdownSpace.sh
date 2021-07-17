#/bin/bash

# echo $1
fileName=`echo $1 | sed 's/\.[^\.]*$//'`
# echo $fileName
# cat $1 | tr '\n' '  \n' > ${fileName}_revised.md
sed 's/$/  /g' $1 > ${fileName}_rev.md

