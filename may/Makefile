SOURCE := $(shell git ls-files '*.py')

all:

list:
	(cd ../SOURCE/pyramid/ ; git ls-files '*.py') \
	| egrep -v '(docs/|tests/)'

lint:
	black .
	flake8 ${SOURCE}

test:
	python ./may.py ../SOURCE/pyramid/