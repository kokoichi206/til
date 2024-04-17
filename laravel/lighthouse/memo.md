## Installation

https://lighthouse-php.com/5/getting-started/installation.html#install-via-composer

``` sh
composer require nuwave/lighthouse
php artisan vendor:publish --tag=lighthouse-schema


cp vendor/nuwave/lighthouse/src/lighthouse.php config/

mkdir -p graphql
cp vendor/nuwave/lighthouse/src/default-schema.graphql graphql/schema.graphql


php artisan lighthouse:ide-helper
```

![](./docs/getting-started.png)

``` sh
composer require mll-lab/laravel-graphql-playground
```

![](./docs/playground.png)

## The Models

https://lighthouse-php.com/tutorial/#the-models

``` sh
php artisan make:model -m Post
php artisan make:model -m Comment

pa migrate
```

## query

``` sh
curl --request POST \
  --url http://localhost:8000/graphql \
  --header 'content-type: application/json' \
  --data '{"query":"query {\n  users {\n    paginatorInfo {\n      count\n      currentPage\n    }\n    data {\n      id\n      name\n      email\n      created_at\n      updated_at\n    }\n  }\n}"}'

{"data":{"users":{"paginatorInfo":{"count":10,"currentPage":1},"data":[{"id":"1","name":"Mariano White","email":"corrine.oreilly@example.com","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"},{"id":"2","name":"Adela Emmerich","email":"rae50@example.net","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"},{"id":"3","name":"Laurie Corwin","email":"lakin.shirley@example.org","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"},{"id":"4","name":"Aglae Pouros","email":"theidenreich@example.com","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"},{"id":"5","name":"Jody Marquardt","email":"luz98@example.com","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"},{"id":"6","name":"Miss Violette Wiegand IV","email":"eichmann.tom@example.net","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"},{"id":"7","name":"Simeon Quitzon","email":"klocko.karolann@example.org","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"},{"id":"8","name":"America Bahringer","email":"alta.waelchi@example.net","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"},{"id":"9","name":"Oran Langosh PhD","email":"leda87@example.com","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"},{"id":"10","name":"Giuseppe Funk","email":"damon.reilly@example.com","created_at":"2024-04-16 14:50:29","updated_at":"2024-04-16 14:50:29"}]}}}
```

### pagination

page, first でやる！

``` sh
{
  users(
    page: 2
    first:3
  ) {
    data {
      id
      name
    }
  }
  posts {
    id
    title
    author {
      name
    }
    comments {
      id
      reply
    }
  }
}
```

## Mutation

``` sh

```


## Links

- [Lighthouse tutorial](https://lighthouse-php.com/tutorial/#what-is-graphql)
  - [paginate](https://lighthouse-php.com/master/api-reference/directives.html#paginate)
