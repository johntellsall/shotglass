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
