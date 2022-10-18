## [Installation](https://openapi-generator.tech/docs/installation/)

- [usage](https://openapi-generator.tech/docs/usage)
- [現在何が対応しているか](./cli_list.yml)

```sh
# install
npm install @openapitools/openapi-generator-cli -g

openapi-generator-cli help

openapi-generator-cli list

openapi-generator-cli help generate

openapi-generator-cli generate -g go --additional-properties=prependFormOrBodyParameters=true \
    -o out -i petstore.yaml

openapi-generator-cli generate \
    -i petstore.yaml \
    -g kotlin-spring \
    -o out \
    --additional-properties=library=spring-boot,beanValidations=true,serviceImplementation=true \
    --import-mappings=DateTime=java.time.LocalDateTime \
    --type-mappings=DateTime=java.time.LocalDateTime

# とりあえずこれで作成はできた
openapi-generator-cli generate \
    -i openapi.yml \
    -g python-fastapi \
    -o out

openapi-generator-cli generate \
    -i openapi.yml \
    -g go-gin-server \
    -o out
```

### FastAPI

[Documentation for the python-fastapi Generator](https://openapi-generator.tech/docs/generators/python-fastapi)
