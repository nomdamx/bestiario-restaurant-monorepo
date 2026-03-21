.PHONY: run freeze upgrade migrations format lint fix

APP = src/main.py

run_old:
	uv run fastapi dev $(APP) --host 0.0.0.0 --port 5000

run:
	uv run uvicorn src.main:socket_app --host 0.0.0.0 --port 5000 --reload

freeze:
	uv pip freeze > requirements.txt

upgrade:
	alembic upgrade head

migrations:
	alembic revision --autogenerate -m "$(m)"

format:
	uv run ruff format .

lint:
	uv run ruff check .

fix:
	uv run ruff check . --fix
	uv run ruff format .