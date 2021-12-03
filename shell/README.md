# Script Memo

## Regular expression

### Case ignore

#### Shell
``` sh
# Use (?i)
$ echo "This this THIS thiS, iii" | grep -oE "this"
this
$ echo "This this THIS thiS, iii" | grep -oE "(?i)this"
This
this
THIS
thiS
# Recovoer case sensitive
$ echo "This this THIS thiS, iii" | grep -oE "(?i)thi(?-i)s"
This
this
```

#### awk
``` sh
$ echo "This this THIS thiS, iii" | awk '{for (i=1; i<NF; i++){ if($i ~ /this/){print $i} }}'
this
# This worked for awk in ubuntu
$ echo "This this THIS thiS, iii" | awk 'BEGIN{IGNORECASE = 1}{for (i=1; i<NF; i++){ if($i ~ /this/){print $i} }}'
This
this
THIS
thiS,
```

