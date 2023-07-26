DBPATH := ../shotglass.db
# DBPATH := alpine.db
SAMPLE_REPOS := ../SOURCE/flask

all:


# help:
# 	awk '/^[a-z]/ && {print $$1}' Makefile
# :::::::: RENDER

plot:
	python3 plot.py $(DBPATH)
	
# :::::::: DATABASE MANAGE

dbsetup:  ## setup database with tables
	-$(RM) $(DBPATH)
	python3 dbsetup.py $(DBPATH)
	sqlite3 -echo $(DBPATH) '.tables'

dbimport:  ## import Alpine packages (APKBUILD) info into database
	python3 import_alpine.py $(DBPATH)

scan_releases:
	python3 ./scan_releases.py $(DBPATH)
	@echo "DONE: summarize with 'make list-pkg-tags.show'"

zap_releases:  ## delete contents of package_tags table
	sqlite3 -echo $(DBPATH) 'delete from package_tags'
	sqlite3 -echo $(DBPATH) 'select count(*) from package_tags' | grep 0


# :::::::: DATABASE QUERY / EXAMPLES

list_versions:  ## list major, minor, and latest versions of packages
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
	echo "SUMMARIZE: 'make list-pkg-tags.show'"
# make list-pkg-tags.show

release-dates:
	jq 'map(.name, .tag_name, .created_at)' < releases.json

# :::::::: UTILITIES

test:  ## run Python tests (dev mode: exit on first error)
	pytest --exitfirst $$(git ls-files 'test*.py')

setup:  ## setup Python virtualenv
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

distclean:
	-$(RM) -rf venv .pytest_cache

%.show: %.sql  ## run SQL report, send to screen (no output file)
	sqlite3 -echo alpine.db < $<

show-all: $(patsubst %.sql,%.show,$(wildcard *.sql))

fastlint:
	PY_SOURCE=$$(git ls-files '*.py') \
	; flake8 $${PY_SOURCE}

format:
	PY_SOURCE=$$(git ls-files '*.py') \
	; isort $${PY_SOURCE} \
	; black $${PY_SOURCE}

# :::::::: DEMOS

plot_demo_scatter:
	python3 plot_demo_scatter.py
	imgcat plot_demo_scatter.png
	
# :::::::: HELPERS

update-alpine:
	git clone --depth=1 https://gitlab.alpinelinux.org/alpine/aports.git