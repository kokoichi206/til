test "hello" {
  if @lib.hello() != "Hello, moonbit!!!" {
    fail!("@lib.hello() != \"Hello, moonbit!!!\"")
  }

  // snapshot test など？で値を更新してくれる！
  // Update test
  inspect!(@lib.hello(), content="3")
}
