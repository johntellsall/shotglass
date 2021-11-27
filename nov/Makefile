SOURCE_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE"
TEST_REPO_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE/coreutils"
SHOT_SOURCE := $(shell git ls-files '*.py')
PYLINT := pylint --disable=W0511,C

all:

# index:
# 	python3 ./build.py index ${TEST_REPO_DIR}

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

nov:
	-$(RM) main.db
	python3 ./build.py index ${TEST_REPO_DIR}
	ls -l main.db
	@echo
	python3 ./build.py info .

nov2:
	python3 ./build.py ctags ${TEST_REPO_DIR}/gl/lib/cl-strtod.c

info:
	python3 ./build.py info .

faststats:
	python3 ./stats.py ${SOURCE_DIR}/{dhcp,flask}
fullstats:
	python3 ./stats.py ${SOURCE_DIR}/flask ${SOURCE_DIR}/*
# python3 ./stats.py ${SOURCE_DIR}/flask ${SOURCE_DIR}/*
