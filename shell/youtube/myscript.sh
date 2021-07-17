#/usr/bin/bash

# VARIABLES
# Uppercase by convention
# NAME='Brad'
# echo "My name is $NAME"
# echo "My name is ${NAME}"

# USER INPUT
# read -p "Enter your name: " NAME
# echo "Hello $NAME, nice to meet you"

# SIMPLE IF STATEMENT
# NEME="Brad"
# if [ "$NAME" == "Brad" ]
# then
#     echo "Your name is Brad"
# fi

# IF-ELSE
# NEME="Brad"
# if [ "$NAME" == "Brad" ]
# then
#     echo "Your name is Brad"
# else
#     echo "Your name is NOT Brad"
# fi

# FILE CONDITIONS
# FILE='text.txt'
# if [ -f "$FILE" ]
# then
#     echo "$FILE is a file"
# else
#     echo "$FILE is NOT a file"
# fi

# CASE STATEMENT
# read -p "Are you 21 or over? Y/N " ANSWER
# case "$ANSWER" in
#     [yY] | [yY][eE][sS])
#         echo "You can have a beer :)"
#         ;;
#     [nN] | [nN][oO])
#         echo "Sorry, no drinking"
#         ;;
#     *)
#         echo "Please enter y/ or n/no"
#         ;;
# esac

# SIMPLE FOR LOOP
# NAMES="Brad Kevin Alice Mark"
# for NAME in $NAMES
#     do
#         echo "Hello $NAME"
# done

# FOR LOOP TO RENAME FILES
# FILES=$(ls *.txt)
# NEW="new"
# for FILE in $FILES
#     do
#         echo "Renaming $FILE to new-$FILE"
#         mv $FILE $NEW-$FILE
# done

# WHILE LOOP - READ THROUGHT A FILE LINE BY LINE
# LINE=1
# while read -r CURRENT_LINE
#     do
#         echo "$LINE: $CURRENT_LINE"
#         ((LINE++))
# done < "./new-1.txt"

# FUNCTION
# function sayHello() {
#     echo "Hello World"

# }
# sayHello

# FUNCTION WITH PARAMS
# function greet() {
#     echo "Hello, I am $1 and I am $2"
# }
# greet "Brad" "36"

# CREATE FOLDER AND WRITE TO A FILE
mkdir hello
touch "hello/world.txt"
echo "Hello World" >> "hello/world.txt"
echo "Created hello/world.txt"