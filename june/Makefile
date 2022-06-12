PY_SOURCE := $(shell git ls-files '*.py')
# IMGCAT := ${HOME}/bin/imgcat
IMGCAT := imgcat
TEST_FILE := ../SOURCE/flask/src/flask/app.py
TEST_BATCH := ../SOURCE/flask/src/flask/*.py

all:

fastlint:
	pyflakes $(PY_SOURCE)

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
	pytest --cov=. --cov-report=term-missing
# PY_SOURCE := $(shell ls -1 *.py)

# all:

# fmt:
# 	black $(PY_SOURCE)
	
# fastlint:
# 	flake8 $(PY_SOURCE)
# 	@echo DONE

# setup:
# 	python3 -m venv .venv
# 	.venv/bin/pip install -qr requirements.txt
