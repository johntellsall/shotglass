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
	sqlite-utils create-table $@ file_hash \
		tag text \
		hash text \
		name text \
		size_bytes integer \
		--not-null hash \
		--not-null name \
		--pk=tag
	sqlite-utils tables $@ --schema -t

git-ls:
	git -C $(TEST_PROJ) ls-tree  -r --long '2.0.0'


# import:
# 	sqlite-utils insert logs.db loglines access.log --convert '
# type, source, _, verb, path, _, status, _ = line.split()
# return {
#     "type": type,
#     "source": source,
#     "verb": verb,
#     "path": path,
#     "status": status,
# }' --lines
