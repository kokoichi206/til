## before

```sh
$ cat mods-available/mpm_worker.conf
# worker MPM
# StartServers: initial number of server processes to start
# MinSpareThreads: minimum number of worker threads which are kept spare
# MaxSpareThreads: maximum number of worker threads which are kept spare
# ThreadLimit: ThreadsPerChild can be changed to this maximum value during a
#                         graceful restart. ThreadLimit can only be changed by stopping
#                         and starting Apache.
# ThreadsPerChild: constant number of worker threads in each server process
# MaxRequestWorkers: maximum number of threads
# MaxConnectionsPerChild: maximum number of requests a server process serves

<IfModule mpm_worker_module>
        StartServers                     2
        MinSpareThreads          25
        MaxSpareThreads          75
        ThreadLimit                      64
        ThreadsPerChild          25
        MaxRequestWorkers         150
        MaxConnectionsPerChild   0
</IfModule>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```

## after

```sh
sudo systemctl restart apache2

sudo service apache2 restart
```

```sh
# worker MPM
# StartServers: initial number of server processes to start
# MinSpareThreads: minimum number of worker threads which are kept spare
# MaxSpareThreads: maximum number of worker threads which are kept spare
# ThreadLimit: ThreadsPerChild can be changed to this maximum value during a
#                         graceful restart. ThreadLimit can only be changed by stopping
#                         and starting Apache.
# ThreadsPerChild: constant number of worker threads in each server process
# MaxRequestWorkers: maximum number of threads
# MaxConnectionsPerChild: maximum number of requests a server process serves

<IfModule mpm_worker_module>
    SeverLimit  250
        StartServers                     10
        MinSpareThreads          75
        MaxSpareThreads          250
        ThreadLimit                      64
        ThreadsPerChild          32
        MaxRequestWorkers         8000
        MaxConnectionsPerChild   10000
</IfModule>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```

## 考えたこと

- Users が線形に伸びているのに対し Response Time も線形に伸びているということは、全く並列に処理ができていない、ということ
- API に対しても画像に対しても同様
  - 原因は Go や DB の並行処理ではなく、Apache 側の処理の捌き方に問題がありそう
