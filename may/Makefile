SOURCE := $(shell git ls-files '*.py')

all:

list:
	(cd ../SOURCE/pyramid/ ; git ls-files '*.py') \
	| egrep -v '(docs/|tests/)'

lint:
	black .
	flake8 ${SOURCE}

test-p: lint
	python ./may.py ../SOURCE/pyramid/
test: lint
	python ./may.py \
	../SOURCE/cpython/ setup.py