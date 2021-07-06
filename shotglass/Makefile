all:

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

# show Django checks, e.g. auto field
check:
	python -Wa manage.py test

demo:
	pyflakes app/management/commands/render.py
	./manage.py render flask

coverage:
	pytest --cov=app app/tests/test_{draw,render}.py
# coverage report -m