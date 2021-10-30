## seq
-f format   Use a printf(3) style format to print each number.  Only the
    E, e, f, G, g, and % conversion characters are valid, along
    with any optional flags and an optional numeric minimum
    field width or precision.  The format can contain character
    escape sequences in backslash notation as defined in ANSI
    X3.159-1989 (``ANSI C89'').  The default is %g.

-w    Equalize the widths of all numbers by padding with zeros as
    necessary.  This option has no effect with the -f option.
    If any sequence numbers will be printed in exponential nota-
    tion, the default conversion is changed to %e.

### usecase
```sh
seq -f %03g 10
001
002
003
004
005
006
007
008
009
010

seq -w 
$ seq -w 97 100
097
098
099
100
```


```sh
echo -e "time\tmid" > market_price; for i in {09..18}; do for j in {00..59}; do quad=`echo "scale=3; (($i-15)*60+$j)^2/1991600" | bc -l`; time=`echo "scale=3; ($i*60+$j)^2" | bc -l`; echo -e "$i:$j:00\t"`echo "scale=3; 111+$quad+0.4*s(0.1*$time)" | bc -l` >> market_price; done; done
```