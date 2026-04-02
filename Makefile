.PHONY: lint run

lint:
	ruff format .
	ruff check . --fix

run:
	uvicorn src.app:app --reload
