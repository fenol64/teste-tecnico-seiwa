all: up

up:
	docker-compose -f ops/docker-compose.yml up -d --build

down:
	docker-compose -f ops/docker-compose.yml down

logs:
	docker-compose -f ops/docker-compose.yml logs -f

shell:
	docker-compose -f ops/docker-compose.yml exec api /bin/bash

install:
	pip install -r requirements.txt

test:
	pytest

seed:
	python3 scripts/seed.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

prometheus:
	@echo "Abrindo Prometheus em http://localhost:9090"
	@xdg-open http://localhost:9090 || open http://localhost:9090 || echo "Acesse: http://localhost:9090"

grafana:
	@echo "Abrindo Grafana em http://localhost:3000"
	@echo "Usuário: admin | Senha: admin"
	@xdg-open http://localhost:3000 || open http://localhost:3000 || echo "Acesse: http://localhost:3000"

pgadmin:
	@echo "Abrindo pgAdmin em http://localhost:5050"
	@echo "Usuário: admin@admin.com | Senha: admin"
	@xdg-open http://localhost:5050 || open http://localhost:5050 || echo "Acesse: http://localhost:5050"

status:
	docker-compose -f ops/docker-compose.yml ps

.PHONY: up down logs test seed install clean shell prometheus grafana pgadmin status