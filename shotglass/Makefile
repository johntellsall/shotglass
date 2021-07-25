IMAGE_CAT:=/Users/johnmitchell/.iterm2/imgcat
SQL:=sqlite3 db.sqlite3

all:

fastlint:
	black .
	flake8 --exclude=app/management/commands,app/migrations,app/tests
	@echo DONE

lint:
	pylint --errors-only --persistent=y $$(git ls-files '*.py')

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

SQL_LINE:=$(SQL) '.mode line'
stats:
	@echo "FLASK FILES"
	$(SQL) 'select count(*) from app_sourcefile where project="flask"'
	@echo "FLASK SOURCE-FILE"
	$(SQL_LINE) 'select * from app_sourcefile where project="flask" limit 1'
	@echo 'FLASK SKELETON (after render)'
	$(SQL_LINE) 'select * from app_skeleton limit 1'
	$(SQL_LINE) 'select count(*) from app_skeleton'

	
# check -- show Django checks, e.g. auto field
check:
	python -Wa manage.py test

# demo2:
# 	./manage.py make_index ../SOURCE/flask/

nuke-reset-db:
	-$(RM) db.sqlite3
	./manage.py migrate
	
# demo: lint
demo:
	./manage.py make_index ../SOURCE/flask
	./manage.py render flask
	./manage.py draw flask
	convert flask_path.png -scale '300%'  zoot.png
	$(IMAGE_CAT) zoot.png

demo2:
	./manage.py make_index ../SOURCE/flask
	./manage.py render flask
	./manage.py draw flask
	convert flask_path.png -scale '300%'  zoot.png
	$(IMAGE_CAT) zoot.png

test test-all:
	pytest --cov=app app/tests/
test-all-nocov:
	pytest app/tests/

# management commands
test-cmds:
	pytest -vv --pyargs app/management/commands

# sniff -- find stinky code not useful for commit
sniff:
	rg --vimgrep --glob '*.py' '(ipdb|breakpoint)'

test-ctags:
	ctags --output-format=json \
	--fields=*-P --extras=* \
	fetch.py \
	| egrep -v ptag
	@echo
	@echo JSON FIELDS
	ctags --output-format=json --list-fields

# PERFORMANCE: mac ~ 40 files per second
# in size order:
DIRS := requests flask pyramid sqlalchemy django
reindex:
	echo $(DIRS) | xargs -I{} -n1 \
		./manage.py make_index ../SOURCE/{}
	./manage.py show all

rerender: 
	echo flask | xargs -I{} -n1 \
		./manage.py render {}

demo-draw:
	./manage.py make_index ../SOURCE/flask
	./manage.py render flask
	./manage.py draw --draw=simple flask
	convert flask_path.png -scale '300%'  zoot.png
	$(IMAGE_CAT) zoot.png
