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