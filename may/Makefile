SOURCE := $(shell git ls-files '*.py')

all:

list:
	(cd ../SOURCE/pyramid/ ; git ls-files '*.py') \
	| egrep -v '(docs/|tests/)'

# NOTE: "pflake8" reads common pyproject.toml for config
lint:
	black .
	pflake8 --max-complexity 10 ${SOURCE}

test: lint
	pytest --exitfirst --cov=may test_may.py

ctags:
	ctags --fields=+zK --excmd=number \
	-o - ../SOURCE/pyramid/pyramid/settings.py

setup:
	pip install -qr ./requirements.txt

mccabe:
	python -m mccabe --min 0 may.py
mccabe2:
	rg --type=py --files ../SOURCE/pyramid/ \
	| egrep -v '(docs|scaffolds|tests)/' \
	| xargs -n1 -I{} sh -c 'echo {} ; python -m mccabe --min 10 {}'

dot:
	python -m mccabe --dot may.py  > may.dot
	dot -Tpng may.dot -omay.png