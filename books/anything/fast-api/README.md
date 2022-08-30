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

``` sh
# これはダメ！
# curl http://127.0.0.1:8000/api/programmers
curl http://127.0.0.1:8000/api/programmers/

# Create table
>>> from app.db.session import Engine
>>> from app.db.models import Base
>>> Base.metadata.create_all(bind=Engine)


curl -X POST -H "Content-Type: application/json" -d '{ "name": "John Doe", "languages": ["Python"], "twitter_id": "hoge" }' http://127.0.0.1:8000/api/programmers/

curl -X POST -H "Content-Type: application/json" -d '{ "name": "John Daniel", "languages": ["Python", "Golang", "JavaScript"], "twitter_id": "hoge.pien.come.on" }' http://127.0.0.1:8000/api/programmers/
```
