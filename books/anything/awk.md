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
