SOURCE_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE"
TEST_REPO_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE/coreutils"
SHOT_SOURCE := $(shell git ls-files '*.py')
PYLINT := pylint --disable=W0511,C

all:

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt
	
# index:
# 	python3 ./build.py index ${TEST_REPO_DIR}
dec:
	python3 ./build.py dec ${TEST_REPO_DIR}

fmt:
	black .

test:
	python3 -m pytest

ftest:
	${PYLINT} cmd_releases.py
	make test

test2:
	pytest list_releases.py

fastlint:
	flake8 --ignore=F401 ${SHOT_SOURCE}
	@echo DONE

lint:
	${PYLINT} ${SHOT_SOURCE}
	@echo DONE

# build-db:
# 	sqlite3 shotglass.db < db.sql
# sqlite3 shotglass.db -cmd '.fullschema'

# nov: fastlint
dec:
	-$(RM) main.db
	python3 ./build.py index ${TEST_REPO_DIR}
	ls -l main.db
	@echo
	python3 ./build.py info .

dec2:
	python3 ./build.py ctags ${TEST_REPO_DIR}/gl/lib/cl-strtod.c

# nov3:
# 	-$(RM) main.db
# 	python3 ./build.py index ${TEST_REPO_DIR}
# 	ls -l main.db
# 	@echo
# 	python3 ./build.py info .

info:
	python3 ./build.py info .

faststats:
	python3 ./stats.py ${SOURCE_DIR}/{dhcp,flask}
fullstats:
	python3 ./stats.py ${SOURCE_DIR}/flask ${SOURCE_DIR}/*
# python3 ./stats.py ${SOURCE_DIR}/flask ${SOURCE_DIR}/*

list:
	du -sh ../SOURCE/*| sort -h

prof:
	@echo "Flask: 11M Python"
	./test-build.sh flask

med-prof:
	./test-build.sh flask
	./test-build.sh cpython

full-prof:
	@echo "Flask: 11M Python / Dnsmasq: 16M C"
	./test-build.sh flask
	./test-build.sh dnsmasq
	@echo "SQLAlchemy 97M Python / CPython: 198M C"
	./test-build.sh sqlalchemy
	./test-build.sh cpython
	@echo "Node 526M Javascript / Postgres 557M C"
	./test-build.sh node
	./test-build.sh postgres
	@echo "Mongo 812M C"
	./test-build.sh mongo

# TODO: ./test-build.sh redis
# TODO: MySQL 3.0G C./test-build.sh mysql-server
