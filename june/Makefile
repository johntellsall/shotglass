PY_SOURCE := $(shell git ls-files '*.py')
# IMGCAT := ${HOME}/bin/imgcat
IMGCAT := imgcat

all:

fastlint:
	pyflakes $(PY_SOURCE)

setup:
	python3 -m venv .venv
	.venv/bin/pip install -qr ./requirements.txt

run:
	.venv/bin/python3 spider.py spider.py
	${IMGCAT} z.png
