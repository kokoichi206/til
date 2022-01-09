## viewModel]

### 下の２つの違いって？
launchIn は、CoroutinesのFlowを使ったもの。

``` kotlin
fun updateBlog() {
    updateBlogUseCase().launchIn(viewModelScope)
}

fun writeIsDevTrue(context: Context) {
    viewModelScope.launch {
        async {
            DataStoreManager.writeBoolean(
                context,
                DataStoreManager.KEY_IS_DEVELOPER,
                true
            )
        }
    }
}
```

