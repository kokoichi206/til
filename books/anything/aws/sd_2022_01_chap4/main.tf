# ローカル値の設定
locals {
  tags = {
    "project"     = var.project_name
    "environment" = var.environment
    "terraform"   = true
  }
}

# SSH ログインのための公開鍵を登録
resource aws_key_pair administrator {
  key_name = "sd-staging-administrator"
  public_key = "ssh-rsa SOMETHINGHERE administrator@sd.local"
  tags = local.tags
}

# SSH ログインのためのセキュリティグループを登録
resource aws_security_group ssh {
  name = "sd-staging-ssh"
  vpc_id = "vpc-0fca7c8fbb8d07c5b"
  tags = local.tags
}
resource aws_security_group_rule ssh_egress {
  security_group_id = aws_security_group.ssh.id
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
  from_port         = 0
  to_port           = 0
  protocol          = "all"
}
resource aws_security_group_rule ingress {
  security_group_id = aws_security_group.ssh.id
  type              = "ingress"
  cidr_blocks       = ["153.240.3.128/32", "52.194.115.181/32", "52.198.25.184/32", "52.197.224.235/32"]
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
}

# Webサーバとして２台のEC2インスタンスを構築
resource aws_instance web {
  count         = 2
  ami           = "ami-0e60b6d05dc38ff11"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.administrator.key_name
  vpc_security_group_ids = [aws_security_group.ssh.id]
  subnet_id     = "${element(["subnet-055a36e44b59902960", "subnet-038fecec7ae366e20"], count.index)}"
  monitoring    = true
  root_block_device {
    volume_type = "gp3"
    volume_size = "20"
  }
  tags = local.tags
}
# resource aws_instance web_2 {
#   ami           = "ami-0e60b6d05dc38ff11"
#   instance_type = "t2.micro"
#   key_name      = aws_key_pair.administrator.key_name
#   vpc_security_group_ids = [aws_security_group.ssh.id]
#   subnet_id     = "subnet-038fecec7ae366e20"
#   monitoring    = true
#   root_block_device {
#     volume_type = "gp3"
#     volume_size = "20"
#   }
#   tags = local.tags
# }

# それぞれのEC2インスタンスにEIP(Elastic IP)を設定
resource aws_eip web {
  instance = "${element(aws_instance.web.*.id, count.index)}"
  vpc = true
  tags = {
    "project"     = "sd"
    "environment" = "staging"
    "terraform"   = true  
  }
}
# resource aws_eip web_2 {
#   instance = aws_instance.web_2.id
#   vpc = true
#   tags = local.tags
# }
