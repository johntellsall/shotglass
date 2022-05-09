SAMPLE := ../SOURCE/flask
# PY_SOURCE := $(wildcard [a-su-z]*.py)
# PY_SOURCE := $(wildcard *.py)

all:

demo:
	./main.py reset-db
	./main.py add-project --limit ../SOURCE/flask
	make summary
# ./main.py add-project --limit ../SOURCE/flask

summary: summary.csv

%.csv: %.sql
	sqlite3 main.db ".read $<"



# TODO: skip sample_code and test_*.py
coverage:
	pytest --cov

# sniff -- find stinky code that shouldn't make a PR
sniff:
	git grep breakpoint '*.py'  && false

# pre-commit
pre-commit: fmt fastlint

pre-push: sniff

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
	flake8 --max-line-length=88 .
	@echo DONE

lint:
	pylint -E --ignore=test_code.py *.py
	@echo DONE
