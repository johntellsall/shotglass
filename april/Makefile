# flask 10 KLOC
# nginx 186 KLOC
SOURCE_MIN := ../SOURCE/flask
SOURCE_MED := ../SOURCE/nginx
SOURCE_ALL := ../SOURCE/{coreutils,dnsmasq,flask,nginx,iproute2}

all:

# sort imports and format by calling the Ruff linter and then the formatter
format:
	ruff check --select I --fix .
	ruff format .
	
run-show:
	venv/bin/python3 ./shotglass.py render --show-macos

min.png: *.py
	make build-min
	venv/bin/python3 ./shotglass.py render --show --out=$@

beer:
	make build-min
	venv/bin/python3 ./shotglass.py render --out=flask.png
	make build-medium
	venv/bin/python3 ./shotglass.py render --out=nginx.png

render:
	venv/bin/python3 ./shotglass.py render

run: run-min run-all

build-min: ## run on simplest/shortest project
	venv/bin/python3 ./shotglass.py build $(SOURCE_MIN)

build-medium:
	venv/bin/python3 ./shotglass.py build $(SOURCE_MED)

# build-all:
# 	venv/bin/python3 ./shotglass.py build $(SOURCE_ALL)

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

clean:
	$(RM) -r __pycache__

test:
	pytest -s --exitfirst --last-failed

# usage: make test TEST=slice2
ktest:
	pytest -sk ${TEST}
