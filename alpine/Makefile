DBPATH := ../shotglass.db
SAMPLE_REPOS := ../SOURCE/flask

all:

# help:
# 	awk '/^[a-z]/ && {print $$1}' Makefile

# :::::::: DATABASE MANAGE

dbsetup:  ## setup database with tables
	-$(RM) $(DBPATH)
	python3 dbsetup.py $(DBPATH)
	sqlite3 -echo $(DBPATH) '.tables'

dbimport:
	python3 import_alpine.py $(DBPATH)

scan_tags:
	python3 ./scan_tags.py $(DBPATH)

# :::::::: DATABASE QUERY / EXAMPLES

list_versions:
	python3 ./list_versions.py $(DBPATH)

summarize_tags:
	python3 ./summarize_tags.py $(DBPATH)

schema:
	sqlite3 -echo $(DBPATH) '.schema *'

show:
	sqlite3 -echo $(DBPATH) '.read show.sql'

ex-list-tags:  ## list remote tags
	git ls-remote --tags https://github.com/tmux/tmux

# :::::::: FILESYSTEM

alpine_stats:  ## show subset of package info
	python3 alpine_stats.py aports/main/*

# :::::::: ALPHA

scan_lines0:
	python3 scan_lines.py $(DBPATH) $(SAMPLE_REPOS)
scan_lines:
	python3 scan_lines.py $(DBPATH) $(wildcard ../SOURCE/[a-z]*)

scan_packages:
	python3 scan_packages.py $(DBPATH)


# :::::::: UTILITIES

test:
	pytest --exitfirst $$(git ls-files 'test*.py')

setup:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

%.txt: %.sql
	sqlite3 -echo alpine.db < $< | tee $@

%.show: %.sql
	sqlite3 -echo alpine.db < $< | head -20

show-all: $(patsubst %.sql,%.show,$(wildcard *.sql))

fastlint:
	PY_SOURCE=$$(git ls-files '*.py') \
	; flake8 $${PY_SOURCE}

format:
	PY_SOURCE=$$(git ls-files '*.py') \
	; isort $${PY_SOURCE} \
	; black $${PY_SOURCE}
