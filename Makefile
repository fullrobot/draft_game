build-docker:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	docker compose up --build -d