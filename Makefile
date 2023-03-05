IMAGE=simple-fast-pic

build:
	docker build --build-arg MODE=production -t $(IMAGE) .

up:
	docker run -it --rm --name $(IMAGE) -p 8080:8080 -v `pwd`:/code $(IMAGE)

run:
	uvicorn src.main:app --port 8080 --reload

run-bot:
	poetry run python src/tg.py