# export PYTHONASYNCIODEBUG=1
# export PYTHONBREAKPOINT=ipdb.set_trace

SAMPLE := ../SOURCE/flask
# PY_SOURCE := $(shell git ls-files './*.py')
PY_SOURCE := $(shell ls -1 *.py)
DBPATH := main.db


all:

demo:
	./main.py add-project --reset-db ../SOURCE/flask
	make demo.show

demo-plot:
	./main.py add-project --reset-db ../SOURCE/flask
	make summary-symbols.show
	python3 plot_sunburst2.py

# flask			  20K LOC Python library
# zulip			 300K LOC Python application
# sqlalchemy	 463K LOC Python library
# odoo			1547K LOC Python office suite	682K files

stats:
	wc -l $$(rg -g '*.py' --files) | tail -1

build-tiny:
	./build.sh flask
build-medium:
	./build.sh zulip
build-huge:
	./build.sh odoo

demo2b:
	./main.py add-project --reset-db --all ../SOURCE/flask
	make summary
	./main.py add-project --all ../SOURCE/pyramid
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
	! git grep breakpoint '*.py'

pre-commit: fmt fastlint

pre-push: sniff check-types

check-types:
	pyright

# FIXME:
run:
	./main.py ls-tags $(SAMPLE)

PYTEST := venv/bin/pytest -vv --showlocals
# --tb=long

# "make test" runs all tests
# "KEYWORD=foo make testk " runs only tests matching "foo"
test:
	$(PYTEST)
testk:
	$(PYTEST) -k $(KEYWORD)
test-all:
	TEST_ALL=1 $(PYTEST)
	
setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install wheel
	venv/bin/pip install -r requirements.txt

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

# show Ctags
demo_ctags:
	ctags -o - --extras=+r --fields=+r sample_code/sample.py
demo_ctags_support:
	ctags --list-roles | grep -Ew '^(C|Python)'