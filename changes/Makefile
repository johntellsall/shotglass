SAMPLE := ../SOURCE/flask

PY_SOURCE := $(shell ls -1 *.py)
DBPATH := main.db
PYTEST := uv run pytest -vv --showlocals
# --tb=long


all:

lines:
	uv run lines.py $(SAMPLE)/tests/test_basic.py
	
square:
	uv run file_square.py sample_code/sample.py
square-full:
	uv run file_square.py $$(find $(SAMPLE))

extreemap:
	uv run extreemap.py
	
changes:
	uv run changes.py ../SOURCE/dnsmasq

show-recent: ## run most recent SQL report
	RECENT=$$(ls -1t *.sql | head -1 | sed -e 's/.sql/.show/') \
	; make $${RECENT}

# demo:
# 	uv run main.py add-project --reset-db $(SAMPLE)
# 	make demo.show

# demo-plot0:
# 	./main.py add-project --reset-db $(SAMPLE)
# 	make summary-symbols.show
# 	python3 plot_sunburst3.py

# demo-plot-flask:
# 	./main.py add-project --reset-db --all $(SAMPLE)
# 	make summary-symbols.show
# 	python3 plot_sunburst3.py


# build-sqla:
# 	./main.py add-project --reset-db ../SOURCE/sqlalchemy
# 	make summary-symbols.show

# demo-plot:
# 	python3 plot_sunburst3.py

# NAME			#FILES	#PYTHON	LOC	DESCRIPTION					FILES-SYM		LOAD-gato
# flask			246		80		17K		Python library			24	2K			1 sec
# zulip		 	6421	1468	282K	Python chat application	689 21K         5 sec
# sqlalchemy	810		589		463K	Python library			254 53K		    6 sec
# odoo			36540	5425	682K	Python office suite	    ? 69K           15 sec

# raw-build-tiny:
# 	uv run ./main.py add-project --reset-db "../SOURCE/flask"

# build-tiny:
# 	./build.sh flask
# build-medium:
# 	./build.sh sqlalchemy
# build-huge:
# 	./build.sh odoo

# demo2b:
# 	uv run main.py add-project --reset-db --all ../SOURCE/flask
# 	make summary
# uv run main.py add-project --all ../SOURCE/pyramid
# make summary

# summary: summary.csv

# pysummary:
# 	uv run ./main.py summary



%.csv: %.sql
	sqlite3 $(DBPATH) ".read $<"

%.show: %.sql  ## run SQL report, send to screen (no output file)
	sqlite3 -echo $(DBPATH) < $<

# TODO: skip sample_code and test_*.py
coverage:
	uv run pytest --cov

# sniff -- find stinky code that shouldn't make a PR
sniff:
	! git grep breakpoint '*.py'

pre-commit: fmt fastlint

pre-push: sniff check-types

# check-types:
# 	pyright


# "make test" runs all tests
# "KEYWORD=foo make testk " runs only tests matching "foo"
test:
	$(PYTEST)
testk:
	$(PYTEST) -k $(KEYWORD)
test-all:
	TEST_ALL=1 $(PYTEST)
	
fmt:
	uv run isort .
	uv run black .

lint:
	uv run ruff check .
lint-some:
	uv run ruff check --output-format=concise changes.py

# lint -- find major errors with core files
# lintv -- verbose: find any issues with any files
# PYLINT := pylint --rcfile=../pylintrc
# lint-full:
# 	$(PYLINT) -E --ignore='test_*.py' $(PY_SOURCE)
# 	@echo DONE
# lintv:
# 	$(PYLINT) $(PY_SOURCE)
# 	@echo DONE

# show Ctags
demo_ctags:
	ctags -o - --extras=+r --fields=+r sample_code/sample.py
demo_ctags_support:
	ctags --list-roles | grep -Ew '^(C|Python)'

# main2:
# 	uv run main2.py ../SOURCE/flask