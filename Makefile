install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

lint:
	poetry run flake8

selfcheck:
	poetry check

check: selfcheck test lint

build:
	poetry build

setup:
	make build
	sh ./build.sh

.PHONY: install test lint selfcheck check build

publish:
	poetry publish --dry-run

package-install:
	 python3 -m pip install --user --force-reinstall dist/*.whl

dev:
	poetry run flask --app page_analyzer.app --debug run --port 5000

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app