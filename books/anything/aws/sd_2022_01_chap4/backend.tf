terraform {
  backend "s3" {
    bucket = "w0o0ps-sd-sample-ap=northest-1-tfstate"
    region = "ap-northeast-1"
    profile = "default"
    key = "terraform.tfstate"
    encrypt = true
  }
}
