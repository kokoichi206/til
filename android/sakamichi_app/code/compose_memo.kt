// ============ Modifier ============
.layout { measurable, constraints -> 
    onIconGroupWidthChange(constraints.maxWidth)
}
.verticalScroll(rememberScrollState())
.offset(y = -profilePictureSize / 2f)

// ============ Func =================
// Kmongo !
Post::userId `in` userIdsFromFollows

