all:

run:
	venv/bin/python3 ./timeline.py

fastlint:
	flake8 .
	@echo DONE

# setup -- install Python requirements
setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r ./requirements.txt

fix:
	venv/bin/isort .
