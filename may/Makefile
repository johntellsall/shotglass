SOURCE := $(shell git ls-files '*.py')

all:

list:
	(cd ../SOURCE/pyramid/ ; git ls-files '*.py') \
	| egrep -v '(docs/|tests/)'

# NOTE: "pflake8" reads common pyproject.toml for config
lint:
	black .
	pflake8 ${SOURCE}

test: lint
	pytest --exitfirst

ctags:
	ctags --fields=+zK --excmd=number \
	-o - ../SOURCE/pyramid/pyramid/settings.py

setup:
	pip install -qr ./requirements.txt