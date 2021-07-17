# hacker folder??
[このサイト](https://www.hackerrank.com/dashboard)の中の[Linuxのシェルについて](https://www.hackerrank.com/domains/shell)のところを勉強

## input
read name
echo 'Welcome' $name

## for loop
{start..end..increment}
for i in {1..99..2};do
echo $i
done

## calculation
read x
read y

echo $((x + y))
echo $((x - y))
echo $((x * y))
echo $((x / y))

### decimal point
formulは数式が書かれたstring
bcだと、適当な桁(scale)で切り捨て、になってる
そこでawkを使う。ここでのawkはただの整形

read formula
echo "scale=5; $formula" | bc | awk '{printf("%0.3f", $1)}'

### calculate mean
read count
ans=0
for ((i=0; i < $count; i++)); do
    read tmp
    ans=$((ans+tmp))
done

echo ${ans} ${count} | awk '{printf("%0.3f", $1/$2)}'


## conditions
read x
read y

if [ $x -gt $y ]; then
    echo 'X is greater than Y'
elif [ $y -gt $x ]; then
    echo 'X is less than Y'
else
    echo 'X is equal to Y'
fi

## switch
read answer

case $answer in
    [yY])
        echo 'YES'
        ;;
    [nN])
        echo 'NO'
        ;;
esac

## equality
read x
read y
read z

ans=0
if [ $x -eq $y ]; then
    ans = $((ans+=1))
fi
if [ $z -eq $y ]; then
    ans = $((ans+=1))
fi
if [ $x -eq $z ]; then
    ans = $((ans+=1))
fi

case $ans in
    0)
        echo 'SCALENE'
        ;;
    1)
        echo 'ISOSCELES'
        ;;
    3)
        echo 'EQUILATERAL'
        ;;
esac

## array
arrays=(
"test.sh arg1"
"test2.sh arg1 arg2"
"test3.sh"
)

for array in "${arrays[@]}"
do
     "${array}"
done

## cut
3,5文字目のみを取り出す
while read var
do
    echo $var | cut -c3,5
done

2-7文字目を取り出す
while read var
do
    echo $var | cut -c2-7
done

while read var
do
    echo $var | cut -c 13-
done

### 先頭20行を表示
- インクリメントがめんどくさい
cnt=0
while read var
do
    if [ $cnt -lt 20 ]; then
        echo $var
    fi
    cnt=$((cnt += 1))
done


## tr
### 複数のスペースを1つにする
```
while read var
do
    echo $var | tr -s " " " "
done
```


## ??
### Tail of a Text File #1
最後20行だけを表示
input が複数行だったから難しい？どうするのがスマートかな
```
declare -a array=()
while read var
do
    array=("${array[@]}[$var")
done
echo "${array[@]}" | tr '[' '\n' | tail -n 20
```

### Tail of a Text File #2
最後の20文字だけを表示
```
declare -a array=()
while read var
do
    array=("${array[@]}[$var")
done
echo "${array[@]}" | tr '[' '\n' | tail -c 20
```

### paste #3
```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]}[$var")
done
echo $array | tr '[' '\t'
```

### paste #4
ここにきて初めて問題文のpasteを使う...
めっちゃ汚いのでもう少しうまくやりたい
```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]}[$var")
done
echo $array | tr '[' '\n' | paste - - -
```

### paste #1
```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]};$var")
done
echo $array
```


## uniq
### uniq #1
```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]};$var")
done
echo $array | tr ';' '\n' | uniq
```

### uniq #2
sedについて理解が深まった
```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]};$var")
done
echo $array | tr ';' '\n' | uniq -c | sed -r 's/^ +//g'
```

### uniq #4
```
awk $0
```
は、行全てを指定する、
2列目以降全部を表示するには、
```
awk '{for(i=2;i<NF;++i){printf("%s ",$i)}print $NF}'
cut -d' ' -f 2-
```
とする。
```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]};$var")
done
echo $array | tr ';' '\n' | uniq -c | sed -r 's/^ +//g' | awk '$1==1 {print $0}' | awk '{for(i=2;i<NF;++i){printf("%s ",$i)}print $NF}'
```







## grep
### -E
正規表現

### -e "x" -e "y"
xもyもORで検索をかけたい時

### grep -A
```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]}[$var")
done
echo $array | tr '[' '\n' | grep -iE -e "the[n]?" -e "that" -e "those"
```



## sed
### sed #1
```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]}[$var")
done
echo $array | tr '[' '\n' | sed 's/ the / this /1'
```

### sed #2
ignore the case
-e で正規表現にした後、[Yy][Ee][Ss]とかにする
```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]}[$var")
done
echo $array | tr '[' '\n' | sed -e 's/[Tt][Hh][Yy] /your /g'
```

### sed #3
sedでヒットした文字列を再利用するのは、少し特殊？
- (と)をエスケープ
- 再利用時は\1とする

```
sed -e 's/\([Tt][Hh][Yy]\) /{\1} /g' hoge.txt 
```

### sed #4
クレジットカードの下4桁だけ表示する問題
- なぜか最終行が消えるので、クリアできてないが...
- 複数行の置換のやり方をもっとスマートにやりたい
    - [これ](https://orebibou.com/ja/home/201708/20170817_001/)はできなかった...

```
declare -a array=()
read var
array=("$var")
while read var
do
    array=("${array[@]}[$var")
done
echo $array | tr '[' '\n' | sed -E 's/[0-9]{4}/****/1' | sed -E 's/[0-9]{4}/****/1'| sed -E 's/[0-9]{4}/****/1' 
```


