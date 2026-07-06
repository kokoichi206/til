variable "region" {
  type    = string
  default = "ap-northeast-1"
}

# Applied to both functions. Flip between 1 (serialized) and 10 (parallel) to
# observe how the parallelism unit changes.
variable "reserved_concurrency" {
  type    = number
  default = 1
}

variable "sleep_ms" {
  type    = number
  default = 5000
}
