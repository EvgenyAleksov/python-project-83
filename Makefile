install:
	poetry install

make dev:
	poetry run flask --app page_analyzer:app --debug run --port 8000

PORT ?= 8000
start:
	poetry run gunicorn --workers=5 --bind=0.0.0.0:$(PORT) page_analyzer:app

build: 
	poetry build

lint:
	poetry run flake8 page_analyzer

schema-load:
	psql page_analyzer < database.sql

connect:
	psql page_analyzer