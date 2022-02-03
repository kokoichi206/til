# memory leak
https://www.youtube.com/watch?v=VvkRe9vP5Oc&ab_channel=PhilippLackner

## memory leak
- GC in Java と関係している
- 破棄されたのにも関わらず、GC が処理してくれない


``` kotlin
Intent(this, SecondActivity::class.java).also {
    startActivity(it)
}
```


