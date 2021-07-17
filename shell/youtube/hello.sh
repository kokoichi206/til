#! /usr/bin/bash
# echo $BASH_VERSION

# SIGNALS AND TRAPS
# ^C is called interapt signal, sig-int command
# ^Z is called suspend signal
# SIGKILL or SIGSTOP canNOT detect
# trap "echo Exit signal is detected" SIGKILL
# trap "echo Exit signal is detected" SIGINT
# echo "pid is $$"
# while (( COUNT < 10 ))
# do
#     sleep 10
#     (( COUNT ++ ))
#     echo $COUNT
# done
# exit 0
# # kill -9 30804...
# trap "echo Exit command is detected" 0
# echo "Hello world"
# exit 0


# READONLY COMMAND
# var=31
# readonly var
# var=50
# echo "var => $var"
# hello(){
#     echo "Hello wworld!"
# }
# readonly -f hello
# hello(){
#     echo "Hello wworld Again"
# }
# readonly
# readonly -p
# readonly -f


# FUNCTION EXAMPLE
# usage(){
#     echo "You need to provide an argument : "
#     echo "usage : $0 file_name"
# }
# is_file_exist(){
#     local file="$1"
#     [[ -f "$file" ]] && return 0 || return 1
# }
# [[ $# -eq 0 ]] && usage
# if ( is_file_exist "$1" )
# then
#     echo "File found"
# else
#     echo "File not found"
# fi


# FUNCTIONS, LOCAL OR GLOBAL
# function print(){
#     # name=$1
#     local name=$1
#     echo "the name is $name"
# }
# quit (){
#     exit
# }
# name="tom"
# echo "the name is $name : Before"
# print Max
# echo "the name is $name : After"
# quit
# print hoge


# BREAK AND CONTINUE
# for (( i=1; i<=10; i++ ))
# do
#     if [ $i -eq 3 -o $i -eq 6 ]
#     then
#         # break
#         echo "meow"
#         continue
#     fi
#     echo "$i"
# done


# SELECT LOOP
# select name in mark john tom ben
# do
#     case $name in 
#         mark)
#             echo mark selected
#             ;;
#         john)
#             echo john selected
#             ;;
#         tom)
#             echo tom selected
#             ;;
#         ben)
#             echo ben selected
#             ;;
#         *)
#             echo "Enter please provide the no. between 1..4"
#     esac
# done
# Enter number you selected


# FOR LOOP
# for VARIABLE in 1 2 3 4 5
# {START..END..INCREMENT}
# for VARIABLE in {1..10..2}
# for (( i=0; i<5; i++ ))
# do
#     echo $(( i*100 ))
# done

# FOR LOOP TO EXECUTE COMMANDS
# for command in ls pwd date
# do
#     echo "-----------$command-----------"
#     $command
# done
# *, でlsと同じようなことしてる？？
# for item in *
# do
#     # if [ -d $item ]
#     if [ -f $item ]
#     then
#         echo $item
#     fi
# done


# UNTIL LOOP
# n=1
# until [ $n -gt 10 ]
# do
#     echo $n
#     n=$(( n+1 ))
# done


# READ A FILE CONTENT
# -r prevents the \ escape 
# while IFS= read -r line
# do
#     echo $line
# done < test.txt

# cat test.txt | while read p
# do
#     echo $p
# done

# while read p
# do
#     echo $p
# done < test.txt


# WHILE LOOPS
# n=1
# while [ $n -le 10 ]
# do
#     # echo $n
#     echo "$n"
#     n=$(( n+1 ))
#     # (( ++n ))
#     sleep 1
# done


# ARRAY VARIABLE
# CAUTION INDEXES
# os=('ubuntu' 'windows' 'kali')
# os[6]='mac'
# unset os[2]
# echo "${os[@]}"
# echo "${os[1]}"
# echo "${!os[@]}"
# echo "${#os[@]}"

# string=dasfdsafsadfasdf
# echo "${string[@]}"
# echo "${string[0]}"
# echo "${string[1]}"


# THE CASE STATEMENT
# vehicle=bike
# case $vehicle in
#     "car" )
#         echo "Rent of $vehicle is 100 dollar" ;;
#     "van" )
#         echo "Rent of $vehicle is 80 dollar" ;;
#     "bike")
#         echo "Rent of $vehicle is 5 dollar" ;;
#     * )
#         echo "Unknown vehicle";;
# esac


# FLOATING POINT MATH
# num1=20.5
# num2=4
# echo "$num1+$num2" | bc
# echo "scale=20;20.5/5" | bc
# num=27
# # use math library of bc by -l flag
# # man -bc
# echo "scale=2;sqrt($num)" | bc -l
# echo "scale=2;3^3" | bc -l


# PERFORM ARITHMETIC OPERATIONS, int
# num1=20
# num2=5
# echo $num1+$num2
# echo $(( num1 + num2 ))
# echo $(( num1 - num2 ))
# echo $(( num1 * num2 ))
# echo $(( num1 / num2 ))
# echo $(( num1 % num2 ))

# echo $(expr $num1 + $num2 )
# echo $(expr $num1 \* $num2 )


# AND OR OPERATORS, Here's 3 ways
# age=25
# # if [ "$age" -gt 18 ] || [ "$age" -lt 30 ]
# # if [ "$age" -gt 18 ] && [ "$age" -lt 30 ]
# # if [[ "$age" -gt 18 && "$age" -lt 30 ]]
# if [ "$age" -gt 18 -o "$age" -lt 30 ]
# if [ "$age" -gt 18 -a "$age" -lt 30 ]
# then
#     echo "valid age"
# else
#     echo "age not valid"
# fi


# FILE OPERATORS
# echo -e "Enter the name of the file : \c"
# read file_name
# if [ -e $file_name ]
# then
#     echo "$file_name found"
# else
#     echo "$file_name not found"
# fi

# file_name=test.txt
# if [ -f $file_name ]
# then
#     if [ -w $file_name ]  # if file is writable
#     then
#         echo "Type some text data. To quit press ctrl+d"
#         cat >> $file_name
#     else
#         echo "The file do not have write permissions"
#     fi
# else
#     echo "$file_name not exists"
# fi


# IF STATEMENT
# count=10

# if [ $count -ne 9 ]
# then
#     echo "condition is true"
# else
#     echo "condition is false"
# fi

# word=abc

# if [ $word == "abc" ]
# then
#     echo "condition is true"
# fi


# PASS ARGUMENTS
# echo $1 $2 ' > echo $1 $2 $3'

# args=("$@")
# # CAUTION the first index
# echo ${args[0]} ${args[1]} ${args[2]}
# echo $@
# echo $#


# BASIC I/O
# echo "Enter names: "
# read name1 name2
# echo "Enterd name : $name1"

# read -p 'username : ' user_var
# read -sp 'password : ' pass_var
# echo
# echo "name is $user_var"
# echo "password is $pass_var"

# echo "Enter names : "
# read
# echo "Names : $REPLY"

