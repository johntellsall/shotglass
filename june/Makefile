PY_SOURCE := $(shell git ls-files '*.py')
# IMGCAT := ${HOME}/bin/imgcat
IMGCAT := imgcat
TEST_FILE := ../SOURCE/flask/src/flask/app.py

all:

fastlint:
	pyflakes $(PY_SOURCE)

setup:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -qr ./requirements.txt

run:
	.venv/bin/python3 spider.py $(TEST_FILE)
	${IMGCAT} z.png

pre-commit: fastlint

test:
	pytest
