## awk
```bash
seq 100 | awk '{if($1 % 15 == 0){print "FizzBuzz"}else if($1 % 3 == 0){print "Fizz"}else if($1 % 5 == 0){print "Buzz"}else{print $1}}'

seq 30 | awk '{if($1 % 3 == 0){a[$1] = "Fizz"}}{if($1 % 5 == 0){a[$1] = a[$1]"Buzz"}}END{for(i=1; i<length(a); i++){if(a[i] != ""){print a[i]}else{print i}}}'
```

## sed
```bash
# 素直なやり方
seq 100 | sed '5~5s@.*@Buzz@' | sed -E '3~3s@[0-9]*([\w]*)@\1Fizz@'

# よく考えないとわからないやり方
seq 100 | sed '5~5s@.*@Buzz@' | sed '3~3s@[0-9]*@Fizz@'
```


