## API

### database
```sh
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer secret_xAIW851LuT2CzgdZkMfCiB1cd3ovWNKgXScXUazEhZq" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2021-05-13" \
  --data '{
    "parent": { "database_id": "446db31c0a7b42989933a8679927d30e" },
    "properties": {
      "Name": {
        "title": [
          {
            "text": {
              "content": "テスト投稿してみる"
            }
          }
        ]
      },
      "なまえだよ": {
       "rich_text": [
        {
     "text": {
     "content": "テスト投稿できましたね"
     }
    }
       ]
      }
    }
  }'
```
