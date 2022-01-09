@Composable
fun DefaultColumn(
    uiState: MemberListUiState,
    viewModel: MemberListViewModel,
    navController: NavController,
    members: MutableList<Member> = uiState.visibleMembers,
) {
    val itemCount = if (members.size % 3 == 0) {
        members.size / 3
    } else {
        members.size / 3 + 1
    }
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colors.background),
//        contentPadding = PaddingValues(20.dp),
    ) {
        for (index in 0 until itemCount) {
            MemberRow(
                rowIndex = index,
                entries = members,
                navController = navController,
                uiState = uiState,
            )
        }
    }
}
