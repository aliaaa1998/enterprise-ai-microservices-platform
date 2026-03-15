.PHONY: up down logs test lint format migrate seed demo clean

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .

migrate:
	alembic upgrade head

seed:
	python scripts/seed_prompts.py

demo:
	bash scripts/demo.sh

clean:
	docker compose down -v
	rm -rf .pytest_cache .ruff_cache
