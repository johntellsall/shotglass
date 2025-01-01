all:

run:
	venv/bin/python3 -m main aports/main/dn*

test:
	pytest -sv
	
clone-alpine:
	git clone --depth=1 https://gitlab.alpinelinux.org/alpine/aports.git

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

run-model:
	venv/bin/python3 -m model