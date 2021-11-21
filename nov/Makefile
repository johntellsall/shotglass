SOURCE_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE"
TEST_REPO_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE/coreutils"

all:

fmt:
	black .

test:
	pytest list_releases.py

lint:
	flake8

# build-db:
# 	sqlite3 shotglass.db < db.sql
# sqlite3 shotglass.db -cmd '.fullschema'

nov: lint
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
