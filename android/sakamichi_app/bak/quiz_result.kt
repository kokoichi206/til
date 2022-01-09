package io.kokoichi.sample.sakamichiapp.presentation.setting

import androidx.compose.foundation.layout.Row
import androidx.compose.material.Text
import androidx.compose.runtime.Composable

@Composable
fun QuizResultsScreen(uiState: SettingsUiState) {
    Row() {
        Text(text = "quiz results screen")

        Text(text = uiState.totalNum.toString())
    }
}
