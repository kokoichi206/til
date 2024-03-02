dc = docker compose

.PHONY: psql
psql:
	$(dc) exec postgres psql -U postgres test-db

.PHONE: db-up
db-up:
	$(dc) up -d

.PHONE: db-down
db-down:
	$(dc) down -v
