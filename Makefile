all: up

up:
	docker-compose -f ops/docker-compose.yml up -d --build

down:
	docker-compose -f ops/docker-compose.yml down

logs:
	docker-compose -f ops/docker-compose.yml logs -f

install:
	pip install -r requirements.txt

test:
	pytest

seed:
	python3 scripts/seed.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

status:
	docker-compose -f ops/docker-compose.yml ps

.PHONY: up down logs test seed install clean