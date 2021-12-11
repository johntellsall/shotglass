SOURCE_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE"
TEST_REPO_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE/coreutils"
SHOT_SOURCE := $(shell git ls-files '*.py')
PYLINT := pylint --disable=W0511,C

all:

# index2 -- import two small C projects
index2: nuke-database
	python3 ./build.py setup .
	@echo
	python3 ./build.py index ${SOURCE_DIR}/memcached
	python3 ./build.py index ${SOURCE_DIR}/dnsmasq

index: nuke-database
	python3 ./build.py index ${TEST_REPO_DIR}

test-sql:
	sqlite3 main.db < test.sql

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt

nuke-database:
	-$(RM) main.db

dec: nuke-database
	python3 ./build.py index ${TEST_REPO_DIR}
	ls -l main.db
	@echo
	python3 ./build.py info .

# dec:
# 	python3 ./build.py dec ${TEST_REPO_DIR}

# # nov: fastlint
# dec:
# 	-$(RM) main.db
# 	python3 ./build.py index ${TEST_REPO_DIR}
# 	ls -l main.db
# 	@echo
# 	python3 ./build.py info .

# dec2:
# 	python3 ./build.py ctags ${TEST_REPO_DIR}/gl/lib/cl-strtod.c

fmt:
	black .

TEST ?= .
test:
	python3 -m pytest -k $(TEST)

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
