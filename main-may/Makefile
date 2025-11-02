SOURCE := $(shell git ls-files '*.py')
IMGCAT := ~/.iterm2/imgcat	

all:

# CODE
#
lint:
	black .
	flake8 ${SOURCE}

test: lint
	pytest --exitfirst --cov=shotglass test_shotglass.py




show-db:
	sqlite3 main.db < show-db.sql


all-images: $(patsubst %.yaml,%.png,$(shell git ls-files 's*.yaml'))

%.png: %.yaml
	python -m shotglass $(shell yq -r .shotglass.project_path < $<)
	mv main.png $@
	$(IMGCAT) $@
	echo DONE

run: lint
	python -m main ../SOURCE/pyramid/
	$(IMGCAT) main.png
	echo DONE

setup:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt

# HELPERS
#
list:
	(cd ../SOURCE/pyramid/ ; git ls-files '*.py') \
	| egrep -v '(docs/|tests/)'


ctags:
	ctags --fields=+zK --excmd=number \
	-o - ../SOURCE/pyramid/pyramid/settings.py

mccabe:
	python -m mccabe --min 0 main.py

mccabe-example:
	rg --type=py --files ../SOURCE/pyramid/ \
	| egrep -v '(docs|scaffolds|tests)/' \
	| xargs -n1 -I{} sh -c 'echo {} ; python -m mccabe --min 10 {}'

