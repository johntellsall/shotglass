all:

run:
	python3 assemble.py dnsmasq.png hello-2.10.png
	imgcat overview.png
# imgcat --width=120 overview.png


get-debian-source:
	python3 get_source.py -C ../SOURCE/ dnsmasq hello libc6 zlib1g adduser redis-server

run-source:
	python3 get_source.py -C ../SOURCE/ hello
	ls -d ../SOURCE/hello*
# python3 get_source.py hello

# python3 srcgrid.py '../SOURCE/dnsmasq'

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

%.show: %.py
	python3  $<
	imgcat --width=50 $(<:.py=.png)

run-scatter:
	python3 -m main scatter
	imgcat --width=50 r_scatter.png

# FIXME: more here
format:
	ruff check --select=E,W,F --fix --ignore E501 test_pack.py

stats:
	wc -l *.py
	
lint:
	ruff check --output-format=concise .

fix-ruff:
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

extract2:
	-$(RM) database.db
	venv/bin/python3 -m main extract2

test-extract2:
	-$(RM) database.db
	venv/bin/python3 -m main extract2 aports/main/bash aports/main/perl

table.html:
	venv/bin/python3 -m main table > $@

%.show: %.sql
	sqlite3 database.db < $<
	
%.show4: %.sql
	sqlite3 database.db < $< \
	| pr --width=100 --omit-header -4

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

import:
	venv/bin/python3 -m main import aports/main/*

# run run-all:
# 	venv/bin/python3 -m main report

import1:
	venv/bin/python3 -m main import aports/main/d*

run1:
	LIMIT=1 venv/bin/python3 -m main report


run-full:
	-$(RM) database.db
	make import run-all

# run-full1 -- full re-import, short run
run-full1:
	-$(RM) database.db
	make import run1

test:
	pytest -sv
	
clone-alpine:
	git clone --depth=1 https://gitlab.alpinelinux.org/alpine/aports.git

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

run-model:
	venv/bin/python3 -m model