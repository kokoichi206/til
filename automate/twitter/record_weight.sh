#!/bin/sh
#if [ -n "$1" ]; then
#	echo $1
#fi

re='^[0-9]+([.][0-9]+)?$'
if [[ $1 =~ $re ]]; then
	echo 'OK'>OK.txt
	echo $1
	if [ $1 -gt 100 ]; then
		echo 'kkk'
#		echo `date +%s` $1 >> weight.txt
		echo "scale=1; $1/10"|bc
		weight=`echo "scale=1; $1/10"|bc`
		echo `date +%s` $weight  >> weight.txt
		python3 tweet.py $weight
	else
		weight=$1
		echo `date +%s` $weight >> weight.txt
		python3 tweet.py $weight
	fi
	# message=$weight
 	gnuplot all_save_weight.plt
	img=all_weight_from_1225.png
	python3 ./line/send.py $weight $img

else
	echo "Enter your weight after 'bash ~~.sh'"
fi
