val current = LocalDateTime.now()
val formatter = DateTimeFormatter.ofPattern("yyyy年 MM月 dd日 HH時 mm分 ss秒")
val formatted = current.format(formatter)

println("Current: $formatted")
