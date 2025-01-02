all:

import:
	venv/bin/python3 -m main import aports/main/*

run1:
	LIMIT=1 venv/bin/python3 -m main report


run run-all:
	venv/bin/python3 -m main report

run-full:
	-$(RM) database.db
	make import run-all

test:
	pytest -sv
	
clone-alpine:
	git clone --depth=1 https://gitlab.alpinelinux.org/alpine/aports.git

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

run-model:
	venv/bin/python3 -m model