you can check where the bash is
```
which bash
```

## 文字変数の比較
"$NAME"=="Brad"
のところ、=の間にスペース入れると正しく判定してくれない？？
挙動よくわからん

## 数値変数の比較
-eq, -nq, -gt, -ge, -lt, -le

## File conditions
-d file: True if the file is a dictionary
-e file: True if the file exists
-f file: True if the provided string is a file
-g file: True if the group id is set on a file
-r file: True if the file is readable
-s file: True if the file has a non-zero size
-u: True if the user id is set on a file
-w: True if the file is writable
-x: True if the file is an executable

## Command
### find related
locate fstab
which cal

### help related
whatis cal
apropos time
man man

### chmod
user, group, everyone
chmod +x file1
chmod 700 file1
chmod 744 file2
chmod 644 file3
chmod 755 file3

### utils
cal
history
rmdir
more file1
less file1
history | less
less | history
id
watch free -h
killall firefox
which google-chrome

## Environment
set | less
printenv | less
ls -a
-> .bashrc, .profile
ssh -X 192. ....
exit


## what I did
.bashrcにsystem-statusをみれるファイル追加した
名前は「chksys」で、~/bin においてある

## IDK
whileループのところ

### input
echo "Enter names: "
read name1 name2
この2つを1行でかくには、-pフラグをつける。
read -p 'username : ' user_var
sをつけると、パスワード用に非表示、サイレント
read -sp 'password : ' pass_var
echo "name is $user_var"

#### 多くの変数をArrayとして受け取る
echo "Enter names : "
read -a names
表示のときは{}で囲む
echo "Names : ${names[0]}"


### Variables
''で囲むと変数きかないけど、""では効く？
"\$1"と'\$1'は別ものか

### pass variable
その数、
echo \$#

### READ A FILE CONTENT
どのようにファイルコンテントを渡すか、2パターン考えられる
cat test.txt | while read p
do
    echo $p
done

while read p
do
    echo $p
done < test.txt

### curly bracket for 'range' in Python
{START..END..INCREMENT}


## shellScript
sleep 1
open a new terminal
```
gnome-terminal &
```

## exit
exit 0 is a success signal

### trap
```
trap "echo Exit command is detected" 0
echo "Hello world"
exit 0
```

## TODO
man -7 signal


