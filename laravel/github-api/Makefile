.PHONY: clear
clear:
	php artisan cache:clear
	php artisan config:clear

.PHONY: serve
serve: clear
	php artisan optimize
	php artisan serve

.PHONY: lint
lint:
	vendor/bin/phpstan --memory-limit=2G

.PHONY: test
test:
	php artisan test

.PHONY: psql
psql:
	docker compose exec postgres psql -U postgres github
