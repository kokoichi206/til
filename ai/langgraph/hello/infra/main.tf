terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

variable "email_address" {
  description = "Email address to subscribe to SNS topic"
  type        = string
}

resource "aws_sns_topic" "send_email_agent_sample" {
  name = "send-email-agent-sample"

  tags = {
    Name        = "send-email-agent-sample"
    Environment = "development"
  }
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.send_email_agent_sample.arn
  protocol  = "email"
  endpoint  = var.email_address
}
