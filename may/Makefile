
SAMPLE := ../SOURCE/flask
# PY_SOURCE := $(shell git ls-files './*.py')
PY_SOURCE := $(shell ls -1 *.py)
DBPATH := main.db


all:

demo:
	./main.py reset-db
	./main.py add-project ../SOURCE/sqlalchemy
	make pysummary

# demo3:
# 	./main.py reset-db
# 	./main.py add-project ../SOURCE/pyramid
# 	make pysummary
# 	./main.py add-project ../SOURCE/sqlalchemy
# 	make pysummary
# 	./main.py add-project ../SOURCE/requests
# 	make pysummary


# demo2:
# 	./main.py reset-db
# 	./main.py add-project ../SOURCE/flask
# 	make pysummary
# 	./main.py add-project ../SOURCE/pyramid
# 	make pysummary

demo2b:
	./main.py reset-db
	./main.py add-project ../SOURCE/flask
	make summary
	./main.py add-project ../SOURCE/pyramid
	make summary

summary: summary.csv

pysummary:
	./main.py summary


%.csv: %.sql
	sqlite3 $(DBPATH) ".read $<"

%.show: %.sql  ## run SQL report, send to screen (no output file)
	sqlite3 -echo $(DBPATH) < $<

# TODO: skip sample_code and test_*.py
coverage:
	pytest --cov

# sniff -- find stinky code that shouldn't make a PR
sniff:
	git grep breakpoint '*.py'  && false

pre-commit: fmt fastlint

pre-push: sniff check-types

check-types:
	pyright

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

# lint -- find major errors with core files
# lintv -- verbose: find any issues with any files
PYLINT := pylint --rcfile=../pylintrc
lint:
	$(PYLINT) -E --ignore='test_*.py' $(PY_SOURCE)
	@echo DONE
lintv:
	$(PYLINT) $(PY_SOURCE)
	@echo DONE

