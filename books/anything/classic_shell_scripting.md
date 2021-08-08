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

```sh
$ echo /bin/*sh

$ ls /bin/*sh

# Echo matching files 
$ echo *

# you can manipulate the last-modification time
$ touch -t 197607040000.00 US-bicentennial
```

/tmp and /var/tmp

df /tmp

### Temporary Files
A common shell-script preamble is:

```sh
umask 077   # Remove access for all but user

TMPFILE=${TMPDIR-/tmp}/myprog.$$

trap 'rm -f $TMPFILE' EXIT
```

This kind of files are readily guessable. To deal with this security issue, filenames must be unpredictable.

USE mktemp command !!!

```sh
$ TMPFILE=`mktemp /tmp/myprog.XXXXXXXXX`
$ ls -l $TMPFILE

# use /dev/random
$ TMPFILE=/tmp/secret.$(cat /dev/urandom | od -x | tr -d ' ' | head -n 1)
```

### Finding Files
- `locate`
  - find filenames quickly

Finding Where Commands Are Stored

```sh
$ type gcc
$ type type
```

Notice that type is an internal shell command, so it knows about aliases and functions as well

If you wanna select, say, files larger than a certain size, or modified in the last three days, belonging to you, or having three or more hard links, you need the find command, one of the most powerful in the Unix toolbox.

find offer as many as 60 different options

Major Options

- \-atime n
  - select files with access times of n days
- \-ctime n
  - select files with inode-change times of n days
- \-follow
  - Follow symbolic links
- \-group g
  - select files in group g
- \-links n
  - select files with n hard links
- \-ls
  - produce a listing similar to the ls long form, rather than just filenames
- \-mtime n 
  - select files with modification times of n days
- \-name 'pattern'
  - select files matching the shell wildcard pattern
- \-perm mask
  - select files matching the specified octal permission mask
- \-prune
  - do not descend recursively into directory trees
- \-size n
  - select files of size n
- \-type t
  - select files of type t, asingle letter: d(directory), f(file), or l(symbolic link)
- \-user u
  - select files owned by user u

Caveats

Because of find's default directory descent, it potentially can take a long time to run in a large filesystem.

```sh
# ASCII sort
$ find . | LC_ALL=C sort

$ find . -ls
$ find . -prune
$ find * -prune   # $ ls -d *

$ find $HOME/. ! -user $USER 2>/dev/null

# And optin (-a)
$ find . -size +0 -a -size -10
# Or optin (-o)
$ find . -size 0 -o -atime +365   # past year
$ find . -size 0 -o -atime -365   # within year
```

### Running Commands: xargs
When find produces a list of files, it is often useful to be able to supply that list as arguments to another command. Normally, this is done with the shell's command substitution feature.

Whenever you write a program or a command that deals with a list of objects, you should make sure that it behaves properly if the list is empty.

```sh
# ensure that it does not hang waiting for terminal input
# if find produces no output
$ grep POSIX_OPEN_MAX /dev/null $(find /usr/include -type f | sort)
```

```sh
# Get system configuration value of ARG_MAX
$ getconf ARG_MAX
1048576
```

The solution to the ARG_MAX problem is provided by xargs: it takes a list of arguments on standard input, one per line, and feeds them in suitably sized groups to another command given as arguments to xargs.

Here is an example that eliminates the obnoxious Argument list too long error:
```sh
$ find /usr/include -type f | xargs grep POSIX_OPEN_MAX /dev/null
```

### Filesystem Space Information

#### The df Command
df(disk free) gives a one-line summary of used and available space on each mounted filesystem.

```sh
$ df -k
$ df -h
```

#### The du Command
show the space usage in one or more directory trees.

df summarizes free soace by filesystem, but does not tell you how much space a particular directory tree requires. That job is done by du (disk usage). Like its companion, df, du's options tend to vary substantially between systems, and its space units also may vary.
-k (kilobyte units) and -s (summarize)

```sh
$ du /tmp
$ du -s /tmp

$ du -h -s /var/log /var/spool /var/tmp
```

### Comparing Files
cmp command, diff command, diff3 command

```sh
$ cmp /bin/cp /tmp/ls
```

It is conventional in using diff to supply the older file as the first argument.
```sh
$ echo Test 1 > test.1
$ echo Test 2 > test.2
$ diff test.[12]  # same as diff test.1 test.2
1c1
< Test 1
---
> Test 2
```

diff's output is carefully designed so that it can be used by other programs. For example, revision control systems use diff no manage the differences between successive versions of files under their management.

### The patch Utility
```sh
$ diff -c test.1 test.2 > test.dif
$ patch < test.dif  # Apply the differences
$ cat test.1
```

### File Checksum Matching
You can get nearly linear performance by using file checksums.

```sh
$ md5sum /bin/l?
```

### Digital Signature Verificatio
gpg command ?


## sec 11, 12
It's occasionally interesting and instructive to reinvent a useful wheel.

Experienced programmers soon develop a feel for what is cheap and what is expensive.

Accurate execution timing has been harder to acquire because typical CPU timers have resolutions of only 60 to 100 ticks per second, which is completely inadequate in an era of GHz processors.

With only one special-puropose program, an afternoon's worth of work created a usable and useful tool. As is often the case, experience with a prototype in shell was then applied to writing a production version in C.


## sec 13
Processes

A process is an instance of a running program. New processes are started by the fork() and execve() system calls, and normally run  until they issue an exit() system call.

Unix systems have always supported multiple processes. Although the computer seems to be doing several things at once, in realitym this is an illusion, unless there are multiple CPUs. What really happens is that each process is permitted to run for a short interval, called a *time slice*, and then the process is temporarily suspended while another waiting process is given a chance to run. Time slices are quite short, usually only a few milliseconds, so humans seldom notice these *context switches* as control is transferred from one process to the kernel and then to another process. Processes themselves are unaware of context switches, and programs need not be written to relinquish control periodically to the operating system.

A part of the operationg-system kernel, called the *scheduler*, is responsible for managing process execution.

### Process Creation
One of the great contributions of Unix to the computing world is that process creation is cheap and easy.

Many programs are started by a shell. Each process initiated by a command shell starts with these guarantees:

- The process has a *kernel context*: data structures inside the kernel that record process-specific information to allow the kernel to manage and control process execution.
- The process has a *private* and *protected*, virtual address space that potentially can be as large as the machine is capable of addressing.
- Three file descriptors (standard input, standard output, and standard error) are already open and ready for immediate use.
- A process started from an interactive shell has a *controlling terminal*, which serves as the default source and destination for the three standard file systems.
- Wildcard characters in command-line arguments have been expanded.
- An environment-variable area of memory exists, containing strings with key/value assignments that can be retrieved by a library call

The private address space ensures that processes cannot interfere with one another, or with the kernel. Operating systems that do not offer such protection are highly prone to failure.

The three already-open files suffice for many programs, which can use them without the burden of having to deal with file opening and closing, and without having to know anything about filename syntax, or filesystems.

Process number 1 is called init, and is described in the init(8) manual pages. A child process whose parent dies prematurely is assigned init as its new parent. This init process exits, the system halts.

top command. On most systems, top requires intimate knowledge of kernel data structures, and thus tends to require updates at each operating system upgrade.

By default, top shows the most CPU-intensive processes at the top of the list, which is usually what you are interested in.

`bg, fg, jobs, wait` are shell commands for dealing with still-running processes created under the current shell.

Four keyboard charactes interrupt *forground processes*. These characters are settable with stty command options, usually to Ctrl-C(intr: kill), Ctrl-Y (dsusp: suspend, but delay until input is flushed), Ctrl-Z (susp: suspend), and Ctrl-\ (quit: kill with *core dump*)

### Process Control and Deletion
The kill command does the job, but it is misnamed. What it really does is send a *signal* to a specified running process, and with two exeptions noted later, signals can be caught by the process and dealt with: it might simply choose to ignore them.

```sh
# list supported signal names
$ kill -l

# Suspend process
$ kill -STOP XXX
# Resume process in 10 hours
$ sleep 36000 && kill -CONT XXX &
```

As a rule, you should give the process a chance to shut down gracefully by sending it a HUP signal first: if that does not cause it to exit shortly, then try the TERM -> KILL signal.

```sh
$ kill -HUP XXX
# if HUP didn't work
$ kill -TERM XXX
$ kill -KILL XXX
```

### Trapping Process Signals
```sh
$ man -a signal
```

In addition to the standard signals listed earlier with kill -l, the shell provides one additional signal for the trap command: EXIT.

```sh
trap 'echo Ignoring HUP ...' HUP
trap 'echo Terminating on USR1 ...; exit 1' USR1

trap 'echo exitting...' EXIT
```

bash, ksh, and zsh provide two more signals for trap: DEBUG and ERR

The most common use of singnal trapping in shell scripts is for cleanup actions that are run when the script terminates, such as removal of temporary files. Code like this trap command invocation is typical near the start of many shell scripts:

```sh
trap 'clean up action goes here' EXIT
```

Setting a trap on the shell's EXIT signal is usually sufficient, since it is handled after all other signals.

```sh
# Find traps in system shell scripts
$ grep '^trap' /usr/bin/*

$ cat /usr/bin/cd 
```

### Process System-Call Tracing
- ktrace, par, strace, trace, or truss

While these tools are normally not used inside shell scripts, they can be helpful for finding out what a process is doing and why it is taking so long. Also, they do not require source code access, or any changes whatsoever to the programs to be traced, so you can use them on any process that you own.

If you are unfamiliar with the names of Unix system calls, you can quickly discover many of them by examination of trace logs. Their documentation is traditionally found in Section 2 of the online manuals; e.g., open(2).

- access(), stat(), unlink()

```sh
$ PS1='traced-sh$ ' strace -e trace=process /bin/sh

traced-sh$ /bin/pwd
clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0xffff8f04cd00) = 3495057
wait4(-1, /home/ubuntu/work
[{WIFEXITED(s) && WEXITSTATUS(s) == 0}], WSTOPPED, NULL) = 3495057
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=3495057, si_uid=1000, si_status=0, si_utime=0, si_stime=0} ---
wait4(-1, 0xfffff834735c, WNOHANG|WSTOPPED, NULL) = -1 ECHILD (No child processes)

traced-sh$ exit
```

- at, crontab, batch

```sh
# List the current crontab schedule
$ crontab -l
```

### The /proc Filesystem
kernel data is made available through a special device driver that implements a standard filesystem interface in the /proc directory, Each running process has a subdirectory there, named with the process number. and inside each subdirectory are various small files with kernel data.

```sh
# see man page
$ man proc

# The -v option causes unprintable characters 
# to be displayed in caret notation
$ cat -v /proc/13936/cmdline
pcmanfm^@--desktop^@--profile^@LXDE^@
# ^@ represents the NUL character.
```

Having process data available as files is convenient and makes the data easily available to programs written in any programming language, even those that lack a system-call interface. For example, a shell script could collect hardware details of CPU, memory, and storage devices from the /proc/*info files on all of the machines in your environment that hace such files, producing reports somewhat like those from the fancy sysinfo command.


## sec 14
Shell Portability Issues and Extensions

Over time, bash has acquired many of the extensions in ksh93, but not all of them. Thus, there is considerable functional overlap, but there are also many differences. This chapter outlines areas where bash and ksh93 differ, as well as where they have common extensions above and beyond the features of the POSIX shell.

### Gotchas
- echo *is not portable*
- OPTIND *can be a local variable*
- ${var:?message} *may not exist*

### The bash shopt Command
shopt command for enabling and disabling optins.

```sh
$ shopt
```

```sh
PS3='terminal? '
select term in gl35a t2000 s531 vt99
do
  if [ -n "$term" ]
  then
    TERM=$term
    echo TERM is $TERM
    export TERM
    break
  else
    echo 'invalid.'
  fi
done
```

### Extended test operators
-[](img/test_op1.png)

-[](img/test_op2.png)

```sh
generate_data | tee >(sort | uniq > sorted_data)\
          >(mail -s 'raw data' joe) > raw_data
```

Process substitution, combined with tee, frees you from the straight "one input, one output" paradigm of traditional Unix pipes, letting you split data into multiple output streams, and coalesce multiple input data streams into one.


## sec 15
Secure Shell Scripts: Getting Started

Unix security is a problem of legendary notoriety.

### Tips for Secure Shell Scripts
- Don't put the current directory(dot) in PATH
- Protect bin directories
- Design before you code
- Check all input arguments for validity
- Check error codes from all commands that can return errors
- Don't trust passed-in environment variables
- Start in a known place
- Use full pathnames for commands
- Use syslog(8) to keep an audit trail
  - `man logger`
- Always quote user input when using that input
- Don't use eval on user input
- Quote the results of wildcard expansion
- Check user iput for metacharacters
- Test your code and read it critically
- Be aware of race conditions
  - If an attacker can execute arbitrary commands between any two commands in your scripts, will it compromise security? If so, find another way to do it.
- Suspect symbolic links
- Have someone elese review your code for mistakes
- Use setgid rather than setuid, if possible
- Use a new user rather than root
- Limit setuid code as much as possible

### Trojan Horses
su..."switch user"


## Appendix
```sh
$ getconf NAME_MAX .
```

The integration of devices into the hierarchical file system was the best idea in Unix

- [Commands to remember](https://doc.lagout.org/operating%20system%20/linux/Classic%20Shell%20Scripting.pdf#page=497)
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
- retrospective
  - looking back on or dealing with past events or situations.
- havoc
  - widespread destruction.
  - "the hurricane ripped through Florida causing havoc"
- myriad
  - a countless or extremely great number of people or things.
- notoriety
  - the state of being famous or well known for some bad quality or deed.
- Glossary
  - an alphabetical list of words relating to a specific subject, text, or dialect, with explanations; a brief dictionary.
