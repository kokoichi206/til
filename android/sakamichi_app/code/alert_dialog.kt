// デフォで 8dp の padding が入っている？
AlertDialog(
    onDismissRequest = onDismissRequest,
    buttons = {
        // TODO: move the modifiers to FlowRow when it supports a modifier parameter
        Box(Modifier.fillMaxWidth().padding(all = 8.dp)) {
            AlertDialogFlowRow(
                mainAxisSpacing = 8.dp,
                crossAxisSpacing = 12.dp
            ) {
                dismissButton?.invoke()
                confirmButton()
            }
        }
    },
    modifier = modifier,
    title = title,
    text = text,
    shape = shape,
    backgroundColor = backgroundColor,
    contentColor = contentColor,
    properties = properties
)