PY_SOURCE := $(shell git ls-files '*.py')
# IMGCAT := ${HOME}/bin/imgcat
IMGCAT := imgcat
TEST_FILE := ../SOURCE/flask/src/flask/app.py
TEST_BATCH := ../SOURCE/flask/src/flask/*.py

all:

fmt:
	isort .
	black .

render:
	python3 ./render.py render NOTYET
stats:
	python3 ./render.py stats NOTYET

fastlint:
	flake8 $(PY_SOURCE)

setup:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -qr ./requirements.txt

run3:
	.venv/bin/python3 label.py $(TEST_FILE)

run1:
	.venv/bin/python3 spider.py $(TEST_FILE)
	${IMGCAT} z.png

run2:
	.venv/bin/python3 spider.py --style=blocks $(TEST_BATCH)
	${IMGCAT} z.png

pre-commit: fastlint

test:
	pytest --cov=. --cov-report=term-missing .
