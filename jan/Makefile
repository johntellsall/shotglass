TEST_PROJ:=../SOURCE/flask

all:

jan:
	python3 ./cmd_import.py ../SOURCE/flask

test-list:
	cd $(TEST_PROJ) \
	; git ls-files -z \
	| xargs -0 -n1 -I{} -- git log -1 --format="%ai {}" {}

fmt:
	black .

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt

# TODO: add project ID
.PHONY: project.db
project.db:
	sqlite-utils create-database $@
	sqlite-utils create-table --replace $@ file_hash \
		tag text \
		hash text \
		path text \
		size_bytes integer \
		--not-null hash \
		--not-null path
	sqlite-utils tables $@ --schema -t

git-ls:
	git -C $(TEST_PROJ) ls-tree  -r --long '2.0.0' > git-ls.dat

stats:
	sqlite-utils query project.db 'select count(*) from file_hash'

OLD_import:
	head -1 git-ls.dat
	@echo
	sqlite-utils insert project.db file_hash git-ls.dat \
	--lines --convert ' \
_mode, _type, hash, size_bytes, path = line.split(); \
return { \
"hash": hash, \
"path": path, \
"size_bytes": size_bytes, \
"tag": "flask-2.0.0", \
}'
	sqlite-utils project.db "select * from file_hash limit 4" --table
