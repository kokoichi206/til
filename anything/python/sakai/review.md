# コードレビュー
- MinutesOnFootFromStation
- tar.gz でまとめる時に、"-"が使えなかったりする
    - プロジェクト名などには使わない方がいい
- gitignore
    - .idea: pycharm とかが作るもの？
    - .pyc
- import * は何を使ってるかが分かりにくいので避ける
- logger
    - pythonの通常のものと違う挙動をするときは、名前を変えてやる
- imgのpathの情報とかは、settings.py にいれる
- try-except
    - 的確な場所にだけかける
- config
    - config_dev.yml
    - config_prod.yml
    - ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
- os.path.join
- from contextlib import suppress
- func-funcは２行空けだっけ？
- class HTMLPage(object):


```
# urljoin とかを使うと、何をしてるかも分かりやすくなる！
>>> from urllib.parse import urljoin
>>> urljoin('http://test', str(1))
'http://test/1'
```
