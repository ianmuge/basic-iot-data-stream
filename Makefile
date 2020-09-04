.PHONY: setup
setup: ## setup env
	pip install --upgrade pip
	pip install kafka-python fastapi[all] uvicorn
setup-local: ## setup debug env
	python3 -m pip install virtualenv
	python3 -m virtualenv ./venv
	venv/Scripts/activate
	setup
destroy-local: ## destroy debug env
	deactivate
up: ## deploy to docker
	docker-compose up
down: ## destroy docker
	docker-compose down
debug: ## run debug engine
	python ./producer/main.py	