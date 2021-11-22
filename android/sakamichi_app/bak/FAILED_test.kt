
// なんでこのテストが失敗するのかわからない。
// SettingTopScreenVersionTest.kt

@Test
    fun onVersionClickedAfterDelay_doesNotDisplaySnackBar() {
        // Arrange
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val expectedStr = context.resources.getString(R.string.developer_success_snack_bar_text)
        composeRule
            .onNodeWithTag(TestTags.SNACK_BAR_TEXT)
            .assertDoesNotExist()
        composeRule
            .onNodeWithTag(TestTags.SETTING_VERSION)
            .performClick()
            .performClick()
            .performClick()
            .performClick()

        // Act
//        runBlocking {
        android.os.SystemClock.sleep(2000L)
        composeRule
            .onNodeWithTag(TestTags.SETTING_VERSION)
            .performClick()

//        }

        // Assert
        composeRule
            .onNodeWithTag(TestTags.SNACK_BAR_TEXT)
            .assertDoesNotExist()
    }