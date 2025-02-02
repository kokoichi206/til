## create job

https://dkron.io/api/#tag/jobs/operation/createOrUpdateJob

``` sh
curl http://localhost:7904/v1/jobs -X POST --json '{
  "name": "what-is-name",
  "displayname": "what is displayname",
  "schedule": "@every 1m",
  "timezone": "Asia/Tokyo",
  "owner": "Platform Team",
  "owner_email": "www",
  "disabled": false,
  "tags": {
    "server": "true"
  },
  "metadata": {
    "office": "Barcelona"
  },
  "retries": 2,
  "concurrency": "allow",
  "executor": "shell",
  "executor_config": {
    "command": "poetry run python scripts/slack.py"
  }
}'
```

## memo

- docker で動かすと、デフォルトでは agent も docker で動かすことになり、環境構築が面倒。。。
- host にそのまま入れることにするか。
