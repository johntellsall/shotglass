PY_SOURCE := $(shell git ls-files '*.py')

all:

fastlint:
	pyflakes $(PY_SOURCE)

setup:
	python3 -m venv .venv
	.venv/bin/pip install -qr ./requirements.txt

run:
	.venv/bin/python3 $(PY_SOURCE)
