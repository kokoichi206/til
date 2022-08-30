```sh
uvicorn app.main:app --reload
```

- http://127.0.0.1:8000/docs
  - OpenAPI Specification

必要なもの

- スキーマ
  - API が入出力するデータ
- ルータ
- CRUD
- Dependency

```
curl http://127.0.0.1:8000/api/programmers
```
