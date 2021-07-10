all:

lint:
	black .
	flake8 --exclude=app/management/commands,app/migrations,app/tests

update-packages:
	pip3 list --outdated --format=freeze | \
	grep -v '^\-e' | cut -d = -f 1 | \
	xargs -n1 pip3 install -U 

loop-check:
	git ls-files '*.py' \
	| entr -cs 'black . && python manage.py check --fail-level=ERROR'

loop-migrate:
	git ls-files '*.py' \
	| entr -cs './manage.py migrate'

loop-index:
	git ls-files '*.py' \
	| entr -cs './manage.py make_index ../SOURCE/flask'

index:
	./manage.py make_index ../SOURCE/flask

show:
	./manage.py show flask

# demo: index show

stats:
	@echo "FLASK FILES"
	sqlite3 db.sqlite3 'select count(*) from app_sourcefile where project="flask"'
# sqlite3 db.sqlite3 <<EOSQL
# select count(*) from app_symbol
# EOSQL
	
# show Django checks, e.g. auto field
check:
	python -Wa manage.py test

demo2:
	./manage.py make_index ../SOURCE/flask/
	
	# pyflakes app/management/commands/render.py
# demo: lint
demo:
	echo ./manage.py render flask
	./manage.py draw flask

test-most:
	ls -1 app/tests/*.py | egrep -v '_(age.py|sg2.py|sizeplot.py)$$' \
	| xargs -t pytest --cov=app
# app/tests/test_{draw,render,spider}.py
# coverage report -m

test-all:
	pytest --cov=app app/tests/

# app/tests/test_age.py
# app/tests/test_draw.py
# app/tests/test_perf.py
# app/tests/test_render.py
# app/tests/test_sg2.py
# app/tests/test_sizeplot.py
# app/tests/test_spider.py
# app/tests/test_views.py

# sniff -- find stinky code not useful for commit
sniff:
	rg --vimgrep '(ipdb|breakpoint)' | egrep -v "Makefile:"
