TEST_PROJ:=../SOURCE/flask

all:

%.csv: %.sql
	sqlite3 jan.db -init $<
	sqlite-utils jan.db "select * from file_hash limit 4" --table

summary:
	sqlite-utils jan.db "select * from file_hash limit 4" --table

sum-code:
	sqlite-utils jan.db "select count(*) from file_hash where path like '%.py'"

zoot:
	sqlite-utils memory proj_summary.csv \
	'select name from proj_summary where language="Python" and size_mb < 500'

jan:
	python3 ./cmd_import.py ../SOURCE/flask
import2:
	python3 ./cmd_import.py ../SOURCE/django
import-all:
	python3 ./cmd_import.py ../SOURCE/{flask,requests,pyramid,sqlalchemy,django}


fastlint:
	flake8 $$(git ls-files '*.py')


test-list:
	cd $(TEST_PROJ) \
	; git ls-files -z \
	| xargs -0 -n1 -I{} -- git log -1 --format="%ai {}" {}

fmt:
	isort .
	black .

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt

# TODO: add project ID
# .PHONY: project.db
# project.db:
# 	sqlite-utils create-database $@
# 	sqlite-utils create-table --replace $@ file_hash \
# 		tag text \
# 		hash text \
# 		path text \
# 		size_bytes integer \
# 		--not-null hash \
# 		--not-null path
# 	sqlite-utils tables $@ --schema -t

git-ls:
	git -C $(TEST_PROJ) ls-tree  -r --long '2.0.0' > git-ls.dat

stats:
	sqlite-utils query project.db 'select count(*) from file_hash'

# OLD_import:
# 	head -1 git-ls.dat
# 	@echo
# 	sqlite-utils insert project.db file_hash git-ls.dat \
# 	--lines --convert ' \
# _mode, _type, hash, size_bytes, path = line.split(); \
# return { \
# "hash": hash, \
# "path": path, \
# "size_bytes": size_bytes, \
# "tag": "flask-2.0.0", \
# }'
# 	sqlite-utils project.db "select * from file_hash limit 4" --table
