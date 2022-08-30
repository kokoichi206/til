package ec2_sg

testdata := {
  "Reservations": [
    {
      "Instances": [
        {
          "InstanceId": "i-aaaa",
          "SecurityGroups": [{ "GroupId": "sg-0000" }],
          "State": { "Name": "running" },
          "Tags": [
            {
              "Key": "Env",
              "Value": "Staging"
            }
          ]
        }
      ]
    }
  ],
  "SecurityGroups": [
    {
      "IpPermissions": [
        {
          "FromPort": 443,
          "IpRanges": [{ "CidrIp": "0.0.0.0/0" }],
          "ToPort": 443
        }
      ],
      "GroupId": "sg-0000"
    }
  ]
}

test_invalid_violation {
  # with input as <テスト用データ>
  "i-aaaa" == invalid with input as testdata
}

test_invalid_net_filtered {
  not invalid with input as json.patch(testdata, [
    {
      "op": "replace",
      "path": "/SecurityGroups/0/IpPermissions/0/IpRanges/0/CidrIp",
      "value": "10.0.0.0/8",
    }
  ])
}
