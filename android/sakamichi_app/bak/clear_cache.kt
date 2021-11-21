package io.kokoichi.sample.sakamichiapp.presentation.setting

import android.content.Context
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.AlertDialog
import androidx.compose.material.Surface
import androidx.compose.material.Text
import androidx.compose.material.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import io.kokoichi.sample.sakamichiapp.presentation.ui.theme.SubColorS
import java.io.File
import java.lang.Exception

@Composable
fun ClearCacheScreen(
    navController: NavController,
) {
    Surface(
        modifier = Modifier
            .fillMaxSize()
    ) {


        val openDialog = remember { mutableStateOf(true) }

        if (openDialog.value) {
            AlertDialog(
                onDismissRequest = { },
                title = {
                    Text(text = "キャッシュ情報を削除しますか？")
                },
                text = {
                    Text("一時的な情報を削除することでストレージに多少の余裕を持たせることができます。")
                },
                buttons = {
                    val buttonPaddingValue = 12.dp
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(all = buttonPaddingValue),
                    ) {
                        val context = LocalContext.current
                        TextButton(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(5.dp))
                                .background(SubColorS),
                            onClick = {
                                openDialog.value = false

                                deleteCache(context)
                                navController.navigateUp()
                            }
                        ) {
                            Text(
                                modifier = Modifier,
                                text = "削除",
                                color = Color.White,
                            )
                        }
                        // Some space same as the start, end and bottom
                        Spacer(modifier = Modifier.width(buttonPaddingValue))
                        TextButton(
                            modifier = Modifier
                                .weight(1f)
                                .border(
                                    width = 1.dp,
                                    color = SubColorS,
                                    shape = RoundedCornerShape(5.dp)
                                ),
                            onClick = { // キャンセルをタップしたとき
                                openDialog.value = false
                                navController.navigateUp()
                            },
                        ) {
                            Text(
                                text = "キャンセル",
                                color = SubColorS,
                            )
                        }
                    }
                },
//                confirmButton = {
//                    val context = LocalContext.current
//                    TextButton(
//                        modifier = Modifier
//                            .clip(RoundedCornerShape(5.dp))
//                            .background(SubColorS),
//                        onClick = {
//                            openDialog.value = false
//
//                            deleteCache(context)
//                            navController.navigateUp()
//                        }
//                    ) {
//                        Text(
//                            modifier = Modifier,
//                            text = "削除",
//                            color = Color.White,
//                        )
//                    }
//                },
//                dismissButton = {
//                    TextButton(
//                        modifier = Modifier
//                            .border(
//                                width = 1.dp,
//                                color = SubColorS,
//                                shape = RoundedCornerShape(5.dp)
//                            ),
//                        onClick = { // キャンセルをタップしたとき
//                            openDialog.value = false
//                            navController.navigateUp()
//                        },
//                    ) {
//                        Text(
//                            text = "キャンセル",
//                            color = SubColorS,
//                        )
//                    }
//                },
            )
        }
    }
}

fun deleteCache(context: Context) {
    try {
        val dir: File = context.cacheDir
        deleteDir(dir)
    } catch (e: Exception) {
        e.printStackTrace()
    }
}

fun deleteDir(dir: File?): Boolean {
    return if (dir != null && dir.isDirectory) {
        val children: Array<String>? = dir.list()
        children?.forEach { child ->
            val success = deleteDir(File(dir, child))
            if (!success) {
                return false
            }
        }
        dir.delete()
    } else if (dir != null && dir.isFile) {
        dir.delete()
    } else {
        false
    }
}