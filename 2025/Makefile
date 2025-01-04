all:

lint:
	ruff check --output-format=concise .

popcon:
	python3 -m main popcon

test-cov:
	coverage run -m pytest *.py
	coverage report -m

extract2:
	-$(RM) database.db
	venv/bin/python3 -m main extract2

table.html:
	venv/bin/python3 -m main table > $@

%.show: %.sql
	sqlite3 database.db < $<

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

run run-all:
	venv/bin/python3 -m main report

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