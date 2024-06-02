# flask 10 KLOC
# nginx 186 KLOC
SOURCE_MIN := ../SOURCE/flask
SOURCE_MED := ../SOURCE/nginx
SOURCE_ALL := ../SOURCE/{coreutils,dnsmasq,flask,nginx,iproute2}

all:

render-all:
	./build-render-all.sh $(SOURCE_ALL)
	
# sort imports and format by calling the Ruff linter and then the formatter
format:
	ruff check --select I --fix .
	ruff format .
	
run-show:
	venv/bin/python3 ./shotglass.py render --show-macos

min.png: *.py
	make build-min
	venv/bin/python3 ./shotglass.py render --show --out=$@

render:
	venv/bin/python3 ./shotglass.py render

run: run-min run-all

build-min: ## run on simplest/shortest project
	venv/bin/python3 ./shotglass.py build $(SOURCE_MIN)

build-medium:
	venv/bin/python3 ./shotglass.py build $(SOURCE_MED)

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

clean:
	$(RM) -r __pycache__

# run all tests: 				make test
# run tests in file: 			make test TEST=test_render.py
# run keyword-matching tests:	make test TESTK=tweak2
test:
ifeq ($(TESTK),)
	pytest -s --exitfirst --last-failed $(TEST)
else
	pytest -s --exitfirst --last-failed -k '$(TESTK)' $(TEST)
endif
