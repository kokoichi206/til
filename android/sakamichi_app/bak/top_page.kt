package io.kokoichi.sample.sakamichiapp.presentation.setting

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.Divider
import androidx.compose.material.Icon
import androidx.compose.material.Text
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowRight
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import io.kokoichi.sample.sakamichiapp.R
import io.kokoichi.sample.sakamichiapp.presentation.ui.theme.Typography

@Composable
fun SettingTopScreen(
    navController: NavController,
) {
    Column(
        modifier = Modifier
            .fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        TopBar()

        LazyColumn {
            item {
                Divider(
                    color = Color.LightGray,
                    thickness = 1.dp
                )
            }
            val navigation = listOf(
                SettingNavigation.UpdateBlog,
                SettingNavigation.QuizResult,
                SettingNavigation.ClearCache,
            )
            items(navigation) { item ->
                SettingRow(
                    text = item.name,
                    onclick = {
                        navController.navigate(item.route)
                    }
                )
                Divider(
                    color = Color.LightGray,
                    thickness = 1.dp
                )
            }
        }
    }
}

@Composable
fun TopBar() {
    Text(
        modifier = Modifier
            .padding(top = 10.dp, bottom = 5.dp),
        text = stringResource(R.string.setting_screen_title),
        style = Typography.h5,
        textAlign = TextAlign.Center,
    )
}

@Composable
fun SettingRow(
    text: String,
    onclick: () -> Unit,
) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(10.dp)
            .clickable {
                onclick()
            },
        contentAlignment = Alignment.CenterEnd,
    ) {
        Text(
            modifier = Modifier
                .fillMaxWidth(),
            text = text,
            style = Typography.body2,
        )
        Icon(
            imageVector = Icons.Default.KeyboardArrowRight,
            contentDescription = "right arrow",
            tint = Color.LightGray,
            modifier = Modifier
                .size(30.dp)
        )
    }
}
