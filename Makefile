.PHONY: install install-dev run test docker-build docker-up lint

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

install-dev: install
	. .venv/bin/activate && pip install -r requirements-dev.txt

run:
	. .venv/bin/activate && streamlit run streamlit_app.py

test:
	. .venv/bin/activate && pytest tests/ -q

docker-build:
	docker compose build

docker-up:
	docker compose up --build
