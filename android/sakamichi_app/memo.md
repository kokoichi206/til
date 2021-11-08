## ハマったところ
hilt での init() は、テスト時にそのままだと Override できない！

そもそも消して、使用側の setUp で準備するように変更した


shasum -a 256 FILE_NAME


### dlib??
```
io.mockk.proxy.MockKAgentException: MockK could not self-attach a jvmti agent to the current VM. This feature is required for inline mocking
```


https://qiita.com/kasa_le/items/dff4c5527e4eba3257f1
