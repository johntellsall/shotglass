IMGCAT := imgcat-iterm2 --legacy

all:

%.run: %.py
	python3 $<

# %.show: %.png
# 	$(IMGCAT) --width 60% $<

%.show: %.py
	python3 $<
	$(IMGCAT) $(<:.py=.png)
# $(IMGCAT) --width 40% $(<:.py=.png)

%.show: %.sql
	sqlite3 database.db < $<
	
%.show4: %.sql
	sqlite3 database.db < $< \
	| pr --width=100 --omit-header -4

run:
	python3 alpine_stackplot.py
	
proj-stats: proj_stats.py
	python3 proj_stats.py ../SOURCE/linux
	
t-import:
	python3 timeline.py import caddyserver/caddy

timeline.png: timeline.py Makefile
	ruff check --output-format=concise timeline.py
	python3 timeline.py plot
	imgcat-iterm2 --legacy timeline.png

plot2: timeline.py Makefile
	ruff check --output-format=concise timeline.py
	python3 timeline.py plot2
	imgcat-iterm2 --legacy redis.png

assemble-all:
	python3 assemble.py *-[0-9]*.png
	imgcat overview.png


top:
	rg -v '(lib|#)' ../dist/by_vote | rg -v '(debian|debconf|dpkg)' | head

# NOTE: not quite right
list-source-sizes:
	ls --sort=size -sh1 ../SOURCE/*orig* | rg -v 'asc$$'

run-source:
	python3 get_source.py -C ../SOURCE/ hello
	ls -d ../SOURCE/hello*

# redis: 112 source files	140k lines
stats:
	find ../SOURCE/redis-7.0.15/ | rg '[cy]$$' /dev/stdin | rg -v '(tests|deps)/' | wc -l

srcgrid-all:
	python3 -m srcgrid $$(ls -1d ../SOURCE/*-*/)
	echo DONE

srcgrid3:
	python3 srcgrid.py '../SOURCE/dnsmasq' '../SOURCE/hello-2.10'
	ls -1l *png

srcgrid:
	python3 srcgrid.py '../SOURCE/hello-2.10'
	imgcat --width=120 output.png

srcgrid2:
	python3 srcgrid.py '../SOURCE/redis-7.0.15'
	imgcat --width=120 output.png

testx:  # Run tests, stop after first failure
	pytest -sv --maxfail=1

run-scatter:
	python3 -m main scatter
	imgcat --width=50 r_scatter.png

# FIXME: more here
format:
	ruff check --select=E,W,F --fix --ignore E501 test_pack.py

stats-py-count:
	wc -l *.py
	
lint:
	ruff check --output-format=concise .

lint-diff:
	ruff check --output-format=concise --diff .

lint-fix:
	ruff check --output-format=concise --fix .

popcon2:
	python3 -m main popcon2
popcon3:
	python3 -m main popcon3
popcon4:
	python3 -m main popcon4

test-cov:
	coverage run -m pytest *.py
	coverage report -m

extract2: ## Extract from many packages, many releases
	-$(RM) database.db
	venv/bin/python3 -m main extract2
	make summary.show


test-extract2:  ## Extract fast: two packages
	-$(RM) database.db
	venv/bin/python3 -m main extract2 aports/main/bash aports/main/perl
	make summary.show

table.html:
	venv/bin/python3 -m main table > $@

import-full:
	-$(RM) database.db
	@echo
	git -C aports sparse-checkout set main/
	@echo
	git -C aports checkout remotes/origin/3.15-stable
	RELEASE=3.15-stable venv/bin/python3 -m main import aports/main/*
	@echo
	git -C aports checkout remotes/origin/3.14-stable
	RELEASE=3.14-stable venv/bin/python3 -m main import aports/main/*
	@echo
	git -C aports checkout remotes/origin/3.10-stable
	RELEASE=3.10-stable venv/bin/python3 -m main import aports/main/*

dbshell:
	sqlite3 database.db

# FIXME:
test-loop:
	pytest -s --maxfail=1 --verbose test_model.py


run1:
	LIMIT=1 venv/bin/python3 -m main report



test:
	pytest -sv

get-debian-source:
	python3 get_source.py --extract -C ../SOURCE/ \
		dnsmasq hello libc6 zlib1g adduser redis-server

get-alpine:
	git clone --depth=1 https://gitlab.alpinelinux.org/alpine/aports.git

import: ## import Alpine packages
	venv/bin/python3 -m main import aports/main/*

import1: ## import Alpine packages (some, for testing)
	venv/bin/python3 -m main import aports/main/d*

run-full:
	-$(RM) database.db
	make import run-all

# run-full1 -- full re-import, short run
run-full1:
	-$(RM) database.db
	make import run1

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

nuke-virtualenv:
	$(RM) -r venv

run-model:
	venv/bin/python3 -m model

# enable image preview
# - URL like "http://localhost:8000/apie.png"
start-preview-server:
	venv/bin/python3 -m http.server --directory .