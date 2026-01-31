all: up

up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec api /bin/bash

install:
	pip install -r requirements.txt

test:
	pytest

seed:
	python3 scripts/seed.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: up down logs test seed install clean shell