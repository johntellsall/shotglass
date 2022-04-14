SAMPLE := ../SOURCE/flask
# SOURCE := 
all:

april:
	./main.py april

run:
	./main.py ls-tags $(SAMPLE)

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

lint:
	pylint -E --ignore=test_code.py *.py
	@echo DONE
