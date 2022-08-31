## [Redoc](https://github.com/Redocly/redoc)

Redoc で OpenAPI を静的ファイルに変換

```sh
npm install -g redoc-cli

redoc-cli bundle openapi.yml --output index.html --options.theme.colors.primary.main=orange
```

### gh-actions で gh-pages にデプロイ

- [gh-pages.yml](../../.github/workflows/gh-pages.yml)
- [デプロイされたファイル](https://kokoichi206.github.io/til/)
