## sec 0
- Django
  - フルスタック
  - ユーザー認証
  - O/R マッパー
  - URL ディスパッチャ
  ...
- FastAPI
  - 非同期処理が実装しやすい
  - OpenAPI -> JSON Schema model
  - API def -> Swagger UI
  - GraphQL, WebSocket

## sec 1
`pip install flake8 black isort mypy`

`curl -L http://www.gitignore.io/api/python,flask,vscode > .gitignore`

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

```
pip install python-dotenv

flask run
flask routes
```

テンプレートエンジンとは、テンプレートと呼ばれる雛形とデータを合成して成果ドキュメントを出力するソフト

```
pip install email-validator
pip install flask-debugtoolbar
pip install flask-mail
```

- Cookie
  - ブラウザに保存された情報とその仕組み
- セッション
  - ユーザーのログイン情報などをサーバーに保存し、一連の処理を継続的に行えるようにする仕組みのこと
- クッキーを使ったセッション管理により、ステートレスなHTTP通信において、一連の処理を継続的に効率よく行う。


## sec 2
- Blueprint
  - アプリを分割するための Flask の機能
- SQLAlchemy
  - Object Relational Mapping


```
pip install flask-sqlalchemy
pip install flask-migrate
```

db migration

```
flask db init

flask db migrate
flask db upgrade
```


``` 
pip install flask-wtf
```


## sec 3
```
pip install flask-login
```


## sec 5
```
flask db migrate 
flask db upgrade

flask shell
```

## todo
~
a
~

## sec 11 
```
pip install pytest 
pytest
pytest test_sample.py
pytest test_sample.py::test_func2
```

conftest.py を使ってフィクスチャを共有する


