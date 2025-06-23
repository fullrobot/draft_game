.PHONY: install run load-db up make-migrations

install:
	uv venv
	uv sync

run:
	uv run fastapi dev app/main.py

load-db:
	python scripts/setup_db.py --input assets/cards.json

up:
	uv pip compile --output-file requirements.txt pyproject.toml
	docker compose up --build -d

make-migrations:
	@if [ -z "$(name)" ]; then \
		echo "Please provide a migration name using 'make make-migrations name=<migration_name>'"; \
		exit 1; \
	fi
	docker compose exec api alembic revision --autogenerate -m "$(name)"