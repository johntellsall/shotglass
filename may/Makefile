all:

list:
	(cd ../SOURCE/pyramid/ ; git ls-files '*.py') \
	| egrep -v '(docs/|tests/)'

test:
	python ./may.py ../SOURCE/pyramid/