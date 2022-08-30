package ec2_sg

# invalid {
invalid = instance.InstanceId {
	instance := input.Reservations[_].Instances[_]
	instance.State.Name == "running"

	tag := instance.Tags[_]
	tag.Key == "Env"
	tag.Value != "Production"

	sg := input.SecurityGroups[_]

	rule := sg.IpPermissions[_]
	rule.FromPort <= 443
	rule.ToPort >= 443
	rule.IpRanges[_].CidrIp == "0.0.0.0/0"

	sg.GroupId == instance.SecurityGroups[_].GroupId
	# print(instance.InstanceId)
}
