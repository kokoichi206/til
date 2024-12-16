```sh
top - 13:34:23 up 51 days, 22:58,  0 users,  load average: 20.60, 11.67, 5.72
Tasks: 264 total,  10 running, 254 sleeping,   0 stopped,   0 zombie
%Cpu(s): 40.0 us, 55.8 sy,  0.0 ni,  1.7 id,  0.1 wa,  0.0 hi,  2.4 si,  0.0 st
MiB Mem :   7811.3 total,    175.6 free,   1316.9 used,   6318.8 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used.   6352.8 avail Mem

# available が本質的に使えるメモリ量
# free + buff/cache が実質使える領域
# ロードテスト中
$ free
              total        used        free      shared  buff/cache   available
Mem:        7998744     1349516      178500       47904     6470728     6504272
Swap:             0           0           0
# ロードテストやめた後
# 全然変わらない？？？
$ free
              total        used        free      shared  buff/cache   available
Mem:        7998744     1358432      167128       47980     6473184     6495280
Swap:             0           0           0
```