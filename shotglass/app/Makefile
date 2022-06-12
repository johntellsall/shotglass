PY_SOURCE := $(shell ls -1 *.py)

all:

fmt:
	black $(PY_SOURCE)
	
fastlint:
	flake8 $(PY_SOURCE)
	@echo DONE

setup:
	python3 -m venv .venv
	.venv/bin/pip install -qr requirements.txt
