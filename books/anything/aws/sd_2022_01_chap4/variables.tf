variable project_name {
  default = "sd"
}
variable environment {
  default = "staging"
}

variable ec2_key_pair {
  default = "ssh-rsa SOMETHINGHERE administrator@sd.local"
}

variable vpc_id {
  default = "vpc-0fca7c8fbb8d07c5b"
}
variable subnet_ids {
  default = ["subnet-055a36e44b59902960", "subnet-038fecec7ae366e20"]
}

variable allowed_ips {
  default = ["153.240.3.128/32", "52.194.115.181/32", "52.198.25.184/32", "52.197.224.235/32"]
}

variable instance_type {
  default = "t2.micro"
}
variable root_volume_type {
  default = "gp3"
}
variable root_volume_size {
  default = "20"
}
