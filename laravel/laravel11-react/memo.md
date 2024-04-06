## breeze

``` sh
composer require laravel/breeze --dev

php artisan breeze:install
 React with Inertia

pa tinker
```

## inertia

Laravel、Vue、Tailwind などを繋げる？


## tinker

```
> \App\Models\Project::count()
= 30

> \App\Models\Task::count()
= 900

> \App\Models\Task::query()->paginate(5)->all()

> \App\Models\User::query()->paginate(5)->all()
```

## Commands

``` sh
pa make:model Project -fm

pa migrate:refresh
pa migrate --seed

pa make:controller ProjectController --resource --model=Project --requests

pa route:list

pa make:resource ProjectResource
```


## Links

- https://heroicons.com/
  - https://github.com/tailwindlabs/heroicons?tab=readme-ov-file#react
