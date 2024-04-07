## TODO

- 外部 API を叩く
- postgresql との接続
- テスト
  - Feature テスト
  - Unit テスト
composer create-project laravel/laravel laravel11-crash-course

## Init

``` sh
brew install php
brew install composer

composer create-project laravel/laravel laravel11-crash-course

# -m indicate creating migration file
php artisan make:model Note -m
```

## Command

``` sh
php artisan serve

php artisan config:publish

pa make:factory NoteFactory --mtodel=Note

pa db:seed

pa make:controller NoteController --resource --model=Note


$ pa make:view note.index

   INFO  View [resources/views/note/index.blade.php] created successfully. 
```

## VSCode

### Extensions

- PHP
  - https://marketplace.visualstudio.com/items?itemName=DEVSENSE.phptools-vscode
- Laravel Blade formatter
  - https://marketplace.visualstudio.com/items?itemName=shufo.vscode-blade-formatter
- Laravel Blade Snippets
  - https://marketplace.visualstudio.com/items?itemName=onecentlin.laravel-blade
- Laravel Extra Intellisense
  - https://marketplace.visualstudio.com/items?itemName=amiralizadeh9480.laravel-extra-intellisense
- Laravel goto view
  - https://marketplace.visualstudio.com/items?itemName=codingyu.laravel-goto-view
- Auto Rename Tag
  - https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag

## Links

- [Youtube: Laravel 11 Tutorial for Beginners - Laravel Crash Course (2024)](https://www.youtube.com/watch?v=eUNWzJUvkCA)
- db faker
  - https://fakerphp.github.io/
