#!/bin/bash
aws ec2 describe-instances > ec2.json
aws ec2 describe-security-groups > security-groups.json
jq -s add ec2.json security-groups.json > input.json
cat input.json | opa eval data.ec2_sg.invalid -I -b release --fail-defined
