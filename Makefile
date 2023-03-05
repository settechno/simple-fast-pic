
run:
	uvicorn src.main:app --port 8080 --reload

run-bot:
	poetry run python src/tg.py