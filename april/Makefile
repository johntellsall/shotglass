SOURCE := ../SOURCE/flask

all:

run:
	./main.py ls-tags $(SOURCE)
	
test:
	.venv/bin/pytest -v

setup:
	python3 -m venv .venv
	.venv/bin/pip install wheel
	.venv/bin/pip install -r requirements.txt

fmt:
	isort .
	black .

fastlint:
	flake8 .
	@echo DONE
