/**
 * TEMP:
 *
 * Formation Hinata part
 */
// Link to formation page
BoxWithConstraints(
    modifier = Modifier
        .wrapContentSize(Alignment.TopStart)
        .weight(1f)
) {
    val boxWidth = with(LocalDensity.current) { constraints.maxWidth.toDp() }
    val boxHeight = with(LocalDensity.current) { constraints.maxHeight.toDp() }

    val length = min(boxWidth, boxHeight)

    Image(
        painter = painterResource(id = R.drawable.refactor),
        contentDescription = null,
        modifier = Modifier
            .size(length)
            .clip(CutCornerShape(5.dp))
            .clickable {
                // Navigate to formations page  (now, only for hinata-zaka)
                navController.navigate("formations") { launchSingleTop = true }
            },
        contentScale = ContentScale.Crop
    )
}