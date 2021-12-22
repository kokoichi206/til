resource "aws_instance" "hello" {
    ami           = "ami-0df99b3a8349462c6"
    instance_type = "t2.micro"

    tags = {
        Name = "hello"
    }
}

provider "aws" {
    profile = "default" # default以外のprofileを利用する場合はこの部分を変更
    region = "ap-northeast-1"
}
