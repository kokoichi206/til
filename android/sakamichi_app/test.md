## UI test

### TextField の placeholder テスト
assertTextEquals ではできなかった

代わりに TextContains を使用

```kotlin
// Assert
composeRule
    .onNodeWithTag(TestTags.REPORT_ISSUE_BODY)
    .assertTextContains(expected)
```



