# シル芸に効く、Awk処方箋

## sec 3
```sh
$ echo "1 2 3" | awk '{for (i = 1; i <= NF; i++) sum += $i; print sum}'
$ echo "${PIPESTATUS[@]}" | tr ' ' '+' | bc 
$ echo "75 180" | awk '{print $1 / ($2 / 100) ^ 2}'

# Filed の再構築
# $1 = $1 で再構築を行なっている
$ echo "0,1,2" | awk -F',' -v OFS=' ' '{$1 = $1; print}'
```

## sec 4
```sh
substr($0, index($0, "b"))

$ grep -o 'b.*'
```

## sec 5
```sh
$ echo '1 + 2 - 3 * 4 / 5' | bc
$ echo '1 + 2 - 3 * 4 / 5' | bc - l

# ~/.bashrc
calc() {
    awk "BEGIN {print $*}"
}

# def of pi (= atan2(0,-0))
$ awk 'BEGIN{print atan2(0, -0)}'

# Caveats
$ awk 'BEGIN {print int(70.21 * 100)}'
```

## sec 6
連想配列

```sh
BEGIN {
    fruit_list = "Apple Orange Banana"
    num_fruits = split(fruit_list, fruits);
    for (i = 1; i <= num_fruits; i++) {
        print i, fruits[i];
    }
}

$ echo -e "aa\nbb\naa" | awk '!a[$0]++'
$ echo -e "aa\nbb\naa" | sort | uniq

$ echo -e "aa\nbb\naa" | awk 'a[$0]++ == 1'
$ echo -e "aa\nbb\naa" | sort | uniq -d
```




## sec 11
````sh
$ echo 'a b c d' | awk -v before='a' -v after='A' 'sub(before, after)'

$ echo 'This is a pen' | awk '{n += NF} END {print n}'

# 中置記法による bc の実装
$ echo '2 / 3' | awk '{system("awk \047 BEGIN {print " $0"}\047")}'

# sort | uniq
$ echo -e 'a\nb\na' | awk '!a[$0]++ {print $0}'
# 後置
$ echo -e 'a\nb\na' | awk '{print a[$0]++, a[$0]}'
```


