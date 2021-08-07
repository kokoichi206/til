## sec6
### readonly, export

The readonly command makes variables read-only; assignments to them become forbidden. This is a good way to create symbolic constants in a shell program;

```sh
$ hours_per_day=24
$ readonly hours_per_day
```

### export 
Much more commanly used is the export command, which puts variables into the *environment*.

POSIX standard allows you to do the assignment and command together:

### parameter expansion
- ${varname:-word}
  - If varname exists and isn't null, return its value: otherwise, return word
  - Purpuse: To return a default value if the variable is undefined.
- ${varname:=word}
  - if varname exists and isn't null, return its value; otherwise, **set it** to word and then return its value
- ${varname:?message}
  - purpose: To catch errors that result from variables being undefined.
  - ${count:?"undefined!"}

POSIX "wildcard patterns"

- ${variable#pattern}
  - ${path#/*/}
- ${variable%pattern}
  - ${path%.*}
- ${#variable}
  - return the length of the variable

### Positional parameters
For historical reasons, you have to enclose the number in braces if it's grater than nine:

```sh
$ filename=${1:-/dev/tty}

while [ $# != 0 ]
do
    case $1 in
    ...
    esac
    shift
done
```

### Special variables
POSIX built-in shell variables

- \#
  - Number of arguments givecuen to current process.
- @
  - Command-line arguments to current process. Inside double quotes, expands to individual arguments.
- \*
  - Command-line arguments to current process. Inside double quotes, expands to single arguments.
- \-(hyphen)
  - Options given to shell on invocation.
- ?
  - Exit status of previous command.
- $
  - Process ID of shell process.
- 0 (zero)
  - The name of the shell program
- !
  - Process ID of last background command.
- ENV
  - Used only by interactive shells upon invocation; the *value* of $ENV is parameter-expanded. The result should be a full pathname for a file to be read and executed at start up.
- HOME
  - Home (login) directory.
- IFS
  - Internal field separator; i.e., the list of characters that act as word separators.
- LANG
  - Default name of current locale; overridden by the othe LC_* variables.
- LC_ALL
  - Name of current locale; overrides LANG and the other LC_* variables.
- LC_COLLATE
  - Name of current locale for character collation (sorting) purposes.
- LC_CTYPE
  - Name of current locale for character class determination during pattern matching.
- LC_MESSAGES
  - Name of current language for output messages.
- LINENO
  - Line number in script of function of the line that just ran.
- NLSPATH
  - The location of message catalogs for messages in the language given by $LC_MESSAGES (XSI).
- PATH
  - Search path for commands.
- PPID
  - Process ID of parent process.
- PS1
  - Primary command prompt string. Default is "$".
- PS2
  - Prompt string for line continuations. Default is "> ".
- PS4
  - Prompt string for execution tracing with set -x.Default is "+ ".
- PWD
  - Current working directory.

The special variable $$ is useful in scripting for creating unique (usually temporary) filenames based on the shell's process ID number.


### Options
```sh
# set flag vars to empty
file= verbose= quiet= long=

while [ $# -gt 0 ]
do
  case $1 in
  -f) file=$2
      shift
      ;;
  -v) verbose=true
      quiet=
      ;;
  -q) quiet=true
      verbose=
      ;;
  -l) long=true
      ;;
  --) shift   # by convention, -- ends optins
      break
      ;;
  -*) echo $0: $1: unrecognized optin >&2
      ;;
  *)  break
      ;;
  esac

  shift
done
```

## sec 7

### File
file descriptors 0, 1, and 2 correspond to standarrd input, standard output, and standard error, respectively.

```sh
$ make 1> results 2> ERRS
$ make > results 2> ERRS  # default descriptor is 1

# &1 means, "wherever file descriptor 1 is.
$ make > results 2>&1
$ make 2>&1 | results   # you can send error down the pipeline
```

exec command may be used to change the **shell's own I/O**

```sh
$ exec 2> /tmp/$0.log       # Use only in a script!!
$ exec 3< /some/file        # Open new file descriptor 3
$ read name rank serno <&3  # Read from that file
```

Other use of exec
```sh
# When used this way, exec is a one-way operation.
# Never returns to the script!!!
exec real-app -q "$qargs" -f "$fargs" "$@"
echo real-app failed, get help! 1>&2    # Emergency message
```

### printf
print format specifiers

| Item | Description |
| --- | --- |
| %b | Th ecorresponding arguments is treated as a string containing escape sequences to be processed. |
| %c | ASCII character. Print the first character of the corresponding argument |
| %d,%i | Decimal integer |
| %e | Floating-point format([-]d.presitione[+-]dd) |
| %E | Floating-point format([-]d.presitionE[+-]dd) |
| %f | Floating-point fomrmat([-]ddd.precision) |
| %g | %e or %f conversion, whichever is shorter, with trailing zeros removed |
| %G | %E or %f conversion, whichever is shorter, with trailing zeros removed |
| %o | Unsigned octal value |
| %s | String |
| %u | Unsigned decimal value |
| %x | Unsigned hexadecimal number. Use a-f for 10-15 |
| %X | Unsigned hexadecimal number. Use A-F for 10-15 |
| %% | Literal% |

you can specify field width

```sh
# string
$ printf "|%10s|\n" hello
|     hello|
$ printf "|%-10s|\n" hello
|hello     |

# number
$ printf "%5d\n" 15
   15
$ printf "%.5d\n" 15
00015
$ printf "%.2f\n" 123.4567
123.46
$ printf "%2f\n" 123.4567   # ?
123.456700
```

Flags for printf
| Character | Description |
| --- | --- |
| - | Left-justify the formatted value within the field.|
| space | Prefix positive values with a space and negative values with a minus |
| + | Always prefix numeric values with a sign, even if the value is positive |
| # | Use an alternate form:%o has a preceding O; 
| 0 (zero) | Pad output with zeros, not spaces. This happens only when the width is wider than the converted result |

```sh
$ printf "|% d| |% d|\n" 15 -15
| 15| |-15|
$ printf "|%+d| |%+d|\n" 15 -15
|+15| |-15|
$ printf "%x %#x\n" 15 15   # # flag
f 0xf
$ printf "%05d\n" 15
00015
```

### Wildcarding
Basic wildcards

| wildcard | Matches |
| ? | Any single character |
| * | Any string of charatcters | 
| [set] | Any character in set |
| [!set] | Any character *not* in set |

### Command Substitution
Command substitution is the process by which the shell runs a command and replaces the command substitution with the output of the executed command.

```sh
# There are two ways

$ echo `ls`

$ echo $(ls)
```

### Subshells and Code Blocks
A subshell is a group of commands enclosed in parentheses. The commands a re run in a separate process.

```sh
$ tar -cf - . | (cd /newdir; tar -xpf -)
```

A code block is conceptually similar to a subshell, but it does not create a new process. Commands in a code block are enclosed in braces, and do affect the main script's state.

| Construct | Delimiters | Recognized where | Separate process |
| -- | --- | --- | --- |
| Subshell | () | Anywhere on the line | Yes |
| Code block | {} | After newline, semicolon, or keyword | No |

You should use a subshell when you want the enclosed commands to run without affecting the main script.

### POSIX shell built-in commands
![](img/built-in1.png)

![](img/built-in2.png)


## sec 8
One of the insidious ways that shell scripts can be attacked is by manipulating the input field separator, IFS, which influences how the shell subsequently interprets its input. (HOW??)

Another comman way to break security is to trick software into executing unintended commands.

Exhaustive testing is tedious!

Because undocumented software is likely to be unusable software, and because few books describe how to write manual pages, we develop a manual page for pathfind in Appendix A.

troff was one of the earliest successful attempts at computer-based typesetting.

Because Unix runs so many different platforms, it is common practice to build software package from source code, rather than installing binary distributions.


## sec 9
Enough awk to Be Dangerous

If no filenames are specified on the command line, awk reads from standard input.

option

- \-\-
  - it indicates that there are no further command-line options for awk itself.
- \-F
  - redifines the default field separator, and it is conventional to make it the first command-line option.
- \-v
  - this options must precede any program given directly on the command line;

awk views an input stream as a collection of records, each of which can be further subdivided into fields

An awk program consists of pairs of patterns and braced actions

- pattern { action }
  - run action if pattern matches
- pattern
  - print record if pattern matches
- { action }
  - run action for every record

two special patterns, BEGIN and END

```awk
s = "ABCD"
s = "AB" "CD"
s = "A" "B" "C" "D"
```

regular expressions

~(matches) and !~(does not match)

"ABC" ~ "^[A-Z]+$" is true

"ABC" ~ /^[A-Z]+$/ same

x != x is true only if x is NaN

awk variable names are case-sensitive: foo, Foo, and FOO are distinct names. a common, and recommended, convention is to name local variables in lowercase, global variables with an initial uppercase letter, and built-in variables in uppercase.

awk provides several built-in variables

Commonly used built-in scalar variables in awk

| Variable | Description |
| --- | --- |
| FILENAME | Name of the current input file |
| FNR | Record number in the current input file |
| FS | Field separator (regular expression)(default:" ") |
| NF | Number of fields in current record |
| NR | Record number in the job |
| OFS | Output fleld separator (default:" ") |
| ORS | Output record separator (default:"\n") |
| RS | Input record separator (default:"\n") |

### Array Variables
Arrays with arbitrary indices are called associative arrays because they associate names with values, much like humans do.

### Command-Line Arguments
ARGC(Argument Count), ARGV(Argument vector, values)
```sh
$ cat showargs.awk
BEGIN {
  print "ARGC =", ARGC
  for (k=0; k<ARGC; k++)
    print "ARGV[" K "] = [" ARGV[k] "]"
}
$ ark -v One=1 -v Two=2 -f showargs.awk Three=3 file1 Four=4 file2 file3
ARGC = 6
ARGV[0] = [awk]
ARGV[1] = [Three=3]
...
```

### Environment Variables
awk provides access to all of the environment variables as entries in the built-in array ENVIRON:

```sh
$ awk 'BEGIN{ print ENVIRON["HOME"]; print ENVIRON["USER"]}'
```

### Fields
Fields are available to the awk program as the special names $1,$2,$3,..$NF.

### Pattern and Actions
Patterns and actions form the heart of awk programming. It is awk's unconventional *data-driven* programming model that makes it so attractive and contributes to the brevity of many awk programs.

#### Patterns

- (FNR == 3) && (FILENAME ~ /[.][ch]$/)
  - select record 3 in C source files
- /[Xx][Mm][Ll]/
  - select records containing "XML", ignoring lettercase

Two expressions separated by a comma select records from one matching the left expression up to, and including, the record that matches the right expression !!!

- (FNR == 3), (FNR == 10)
  - select records 3 through 10 in each input file
- /<[Hh][Tt][Mm][Ll]>/, /<\/[Hh][Tt][Mm][Ll]>/
  - select body of an HTML document

### One-Line Programs in awk
```sh
# wc command using awk
$ awk '{ C += length($0) + 1; W += NF}END{ print NR, W, C}'

# this is equal to `cat fileA`
$ awk 1 fileA

```

### Statements
```sh
if (expression)
  statement1
else
  statement2

$ awk 'BEGIN { for (x=0; x<=1; x += 0.05) print x}'
```

It is important to distinguish finding an index from finding a particular value. The index membership test requires constant time, whereas a search for a value takes time proportional to the number of elements in the array/


### User-Controlled Input
```awk
print "What is the square root of 625?"
getline answer
print "Your reply, ", answer ", is", (answer == 25)? "right.": "wrong."
```

### system() function
```awk
system("rm -f " tmpfile)
```

### String Functions
- substring extraction
  - substr(string, start, len)
- lettercase conversion
  - tolower(string)
  - toupper(string)
- string searching
  - index(string, find)
    - index("abcdef", "de") returns 4
    - index(tolower(string), tolower(find))
    - returns 0 if find is not found in string
- string matching
  - match(string, regexp)
- string substitution
  - sub(regexp, replacement, target)
  - gsub(...)
- string splitting
  - split(string, array, regexp)
  - breaks string into pieces stored in successive elements

### Numeric Functions
- atan2(y, x)
  - return the arctangent of y/x as a value in -pi to +pi
- cos(x)
- exp(x)
- int(x)
- log(x)
- rand()
  - return a uniformaly distributed pseudorandom number, r, such that 0 <= r < 1
- sqrt(x)
  - return the square root of x
- srand(x)
  - set the pseudorandom-number generator seed to x, and return the current seed. if x is omitted, use the current time in seconds, relative to the system epoch. If srand() is not called, awk starts with the same default seed on each run; mawk does not.

```
base ❯ for k in 1 2 3 4 5
… for ❯ do
… for ❯ awk 'BEGIN {
… for quote ❯ srand()
… for quote ❯ for (k=1; k<=5; k++)
… for quote ❯ printf("%.5f ", rand())
… for quote ❯ print ""
… for quote ❯ }'  
… for ❯ sleep 1
… for ❯ done
0.00248 0.23986 0.09344 0.51216 0.89200 
0.36665 0.15769 0.90188 0.33921 0.83178 
0.72635 0.57173 0.20648 0.66097 0.76693 
0.57870 0.97954 0.00067 0.47364 0.19478 
0.93932 0.89441 0.80636 0.79652 0.13092 
```

## sec 10
Working with Files

## Memo

### To search
- expr

### words
- caveats
  - a warning to consider something before taking any more action, or a statement that limits a more general statement:
- sloppy
  - not taking care or making an effort:
  - Spelling mistakes always look sloppy in a formal letter.
- sanity check
  - a basic test to quickly evaluate whether a claim or the result of a calculation can possibly be true.
- pitfalls
- ternary
  - consisting of three parts
