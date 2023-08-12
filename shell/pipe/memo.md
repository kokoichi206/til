``` sh
strace -f -o bash-raw bash -c 'echo hoge'
strace -f -o bash-pipe bash -c 'echo hoge | grep o'


strace -f -o bash-pipe-pipe bash -c 'echo hoge | grep o | grep e'

strace -f -o bash-pipe-pipe-pipe bash -c 'echo hoge | grep o | grep e | grep h'



strace -f -o bash-pipe-fail bash -c 'echo hoge | grep p'

strace -f -o bash-pipe-success-fail bash -c 'echo hoge | grep o | grep p'

```
