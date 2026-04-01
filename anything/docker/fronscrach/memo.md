Learned from https://www.youtube.com/watch?v=8fi7uSYlOdc

## Container

- Namespaces
- Chroot
- Cgroups
  - What u can use
  - Filesystem interface
    - memory
    - cpu
    - io
    - process number
    - ...

```sh
❯ docker run --rm -it ubuntu /bin/bash
root@76721b7fec3b:/# hostname
76721b7fec3b
root@76721b7fec3b:/# ps
    PID TTY          TIME CMD
      1 pts/0    00:00:00 bash
     10 pts/0    00:00:00 ps
```

``` sh
ls -l /proc/self/exe

lrwxrwxrwx 1 kokoichi users 0 Apr  1 10:30 /proc/self/exe -> /nix/store/vk82nqvwxcwbansy86kn1f8nvr8219n7-coreutils-full-9.8/bin/coreutils


[kokoichi@nixos:~/work/container]$ ls -l /proc/self
lrwxrwxrwx 1 root root 0 Mar 29 04:47 /proc/self -> 356657
```

``` sh
ps -C sleep

```

## cgroup

``` sh
[kokoichi@nixos:~/work/container]$ cd /sys/fs/cgroup/

[kokoichi@nixos:/sys/fs/cgroup]$ ls
cgroup.controllers      cpu.pressure           init.scope     kubepods                misc.peak
cgroup.max.depth        cpuset.cpus.effective  io.cost.model  memory.numa_stat        sys-fs-fuse-connections.mount
cgroup.max.descendants  cpuset.cpus.isolated   io.cost.qos    memory.pressure         sys-kernel-config.mount
cgroup.pressure         cpuset.mems.effective  io.pressure    memory.reclaim          sys-kernel-debug.mount
cgroup.procs            cpu.stat               io.prio.class  memory.stat             sys-kernel-tracing.mount
cgroup.stat             cpu.stat.local         io.stat        memory.zswap.writeback  system.slice
cgroup.subtree_control  dev-hugepages.mount    irq.pressure   misc.capacity           user.slice
cgroup.threads          dev-mqueue.mount       k3s            misc.current


[kokoichi@nixos:/sys/fs/cgroup]$ cat memory.stat 
anon 2049646592
file 9518583808
kernel 925802496
kernel_stack 7421952
pagetables 35082240
sec_pagetables 0
percpu 1328040
sock 24576
vmalloc 1527808
shmem 18305024
zswap 0
zswapped 0
file_mapped 761057280
file_dirty 372736
file_writeback 0
swapcached 12288
anon_thp 0
file_thp 0
shmem_thp 8388608
inactive_anon 5353472
active_anon 2052427776
inactive_file 8647675904
active_file 852815872
unevictable 9949184
slab_reclaimable 864684480
slab_unreclaimable 13514760
slab 878199240
workingset_refault_anon 0
workingset_refault_file 4247
workingset_activate_anon 0
workingset_activate_file 4236
workingset_restore_anon 0
workingset_restore_file 26
workingset_nodereclaim 1536
pgdemote_kswapd 0
pgdemote_direct 0
pgdemote_khugepaged 0
pgpromote_success 0
pgscan 1629223
pgsteal 1570393
pgscan_kswapd 1619463
pgscan_direct 9760
pgscan_khugepaged 0
pgsteal_kswapd 1561315
pgsteal_direct 9078
pgsteal_khugepaged 0
pgfault 2567200536
pgmajfault 2890
pgrefill 215649
pgactivate 2344
pgdeactivate 0
pglazyfree 3686
pglazyfreed 0
swpin_zero 0
swpout_zero 0
zswpin 0
zswpout 0
zswpwb 0
thp_fault_alloc 0
thp_collapse_alloc 0
thp_swpout 0
thp_swpout_fallback 0
numa_pages_migrated 0
numa_pte_updates 0
numa_hint_faults 0
```

``` sh
[kokoichi@nixos:/sys/fs/cgroup]$ docker run --rm -it ubuntu /bin/bash

docker run --rm -it --memory=10M ubuntu /bin/bash
```

### v2

cgroup v2

``` sh
[kokoichi@nixos:~/work/container]$ stat -fc %T /sys/fs/cgroup
cgroup2fs
```

``` sh
sh-5.3# cat /sys/fs/cgroup/cgroup.controllers
cpuset cpu io memory hugetlb pids rdma misc
```

``` sh
# sleep 100 in container

[kokoichi@nixos:~/work/container]$ cd /sys/fs/cgroup/kk/

[kokoichi@nixos:/sys/fs/cgroup/kk]$ cat cgroup.procs 
416045
416051

[kokoichi@nixos:/sys/fs/cgroup/kk]$ ps -C sleep
    PID TTY          TIME CMD
 420016 ?        00:00:00 sleep
 420310 pts/3    00:00:00 sleep
1737792 ?        00:00:00 sleep

[kokoichi@nixos:/sys/fs/cgroup/kk]$ cat cgroup.procs 
416045
416051
420310


cat pids.current
```
