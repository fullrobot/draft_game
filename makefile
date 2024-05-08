# Define the default behavior of `make` when no target is specified
.DEFAULT_GOAL := help

# Ensure that these targets are not treated as files
.PHONY: make_db build up migrate down help

# Target for creating or recreating the database
make_db:
	psql -c 'DROP DATABASE IF EXISTS draft_game'
	psql -c 'CREATE DATABASE draft_game'

# Target for building Docker containers
build:
	docker compose -f local.yml -f docs.yml build

# Target for starting up Docker containers
up:
	docker compose -f local.yml -f docs.yml up -d

# Target for running migrations
migrate:
	docker compose -f local.yml run --rm django python manage.py makemigrations
	docker compose -f local.yml run --rm django python manage.py migrate

# Target for stopping and removing Docker containers
down:
	docker compose -f local.yml -f docs.yml down

create_superuser:
	docker compose -f local.yml run --rm django python manage.py createsuperuser

# Help target to display usage information
help:
	@echo "Available targets:"
	@echo "  make make_db      : Create or recreate the database"
	@echo "  make build        : Build Docker containers"
	@echo "  make up           : Start up Docker containers"
	@echo "  make migrate      : Run database migrations"
	@echo "  make down         : Stop and remove Docker containers"

# Catch and print a message for undefined targets
%:
	@true
