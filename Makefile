.PHONY: up down reset test-python test-frontend test-gateway test zip

up:
	docker compose up --build

down:
	docker compose down

reset:
	docker compose down -v

test-python:
	cd backend && python -m pytest

test-frontend:
	cd frontend && npm install && npm run build

test-gateway:
	cd gateway && mvn -B test package

test: test-python

zip:
	cd .. && zip -r docmind-enterprise-rag-platform.zip docmind-enterprise-rag-platform -x "*/node_modules/*" "*/target/*" "*/.venv/*" "*/__pycache__/*"
