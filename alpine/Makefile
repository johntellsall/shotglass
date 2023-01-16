DBPATH := ../shotglass.db

all:

# help:
# 	awk '/^[a-z]/ && {print $$1}' Makefile

dbsetup:  ## setup database with tables
	python3 dbsetup.py $(DBPATH)
	sqlite3 -echo $(DBPATH) '.tables'

dbimport:
	python3 import_alpine.py $(DBPATH)
	
# TODO: needs "alpine" table
scan_tags:
	python3 ./scan_tags.py $(DBPATH)

# :::::::: FILESYSTEM

alpine_stats:  ## show subset of package info
	python3 alpine_stats.py aports/main/*

# :::::::: FIXME:

scan_packages:
	python3 scan_packages.py

list_versions:
	python3 ./list_versions.py

# list remote tags
ex-list-tags:
	git ls-remote --tags https://github.com/tmux/tmux


show:
	sqlite3 -echo alpine.db '.read show.sql'
show2:
	clear
	sqlite3 -echo alpine.db '.read show2.sql'

test:
	pytest --exitfirst $$(git ls-files 'test*.py')

setup:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

%.txt: %.sql
	sqlite3 -echo alpine.db < $< | tee $@

%.show: %.sql
	sqlite3 -echo alpine.db < $< | head -20

# TODO: fix output, add header
github-packages.csv: gh-package-list.sql Makefile
	sqlite3 alpine.db < $< > .gh-packages.csv
	awk -F/ '{print $$4"/"$$5 " -- "$$0}' .gh-packages.csv | head -5
	# head -5 $@

format:
	PY_SOURCE=$$(git ls-files '*.py') \
	; isort $${PY_SOURCE} \
	; black $${PY_SOURCE}
