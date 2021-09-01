# Part2

### sed
```sh
$ sed "s/Windows XP/Windows/gi"

$ sed "s/^( +)-/\1*/"
```

### find
```sh
$ find /logs/ -ctime +7 -and -ctime -15
$ find /logs/ -ctime +180 -and -name "*access*"
$ find /logs/ -ctime +30 -and \( -name "*access*" -or -name "*error*" \)
```

### そのほか
```sh
$ prepare-data && process-data && report-result

find /data/backup -ctime +30 | while read file
do
    rm "$file"
done
```
