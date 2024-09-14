PORT ?= 8000

install:
	poetry install

build: 
	poetry build

lint:
	poetry run flake8 page_analyzer

make dev:
	poetry run flask --app page_analyzer:app --debug run --port 8000

database: db-create schema-load

db-create:
	createdb page_analyzer || echo 'skip'

schema-load:
	psql page_analyzer < database.sql

connect:
	psql page_analyzer

start:
	database.sql
	poetry run gunicorn --workers=5 --bind=0.0.0.0:$(PORT) page_analyzer:app
