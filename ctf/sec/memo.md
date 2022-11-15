socket をプロキシする

```sh
socat TCP-L:10042,fork,reuseaddr EXEC:"./server.py"
```
