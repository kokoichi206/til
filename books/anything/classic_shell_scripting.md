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
  - Number of arguments giben to current process.
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


## Memo

### words
- caveats
  - a warning to consider something before taking any more action, or a statement that limits a more general statement:
- sloppy
  - not taking care or making an effort:
  - Spelling mistakes always look sloppy in a formal letter.

