TEST_REPO_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE/coreutils"

all:

test:
	pytest list_releases.py

lint:
	flake8

build-db:
	sqlite3 shotglass.db < db.sql
# sqlite3 shotglass.db -cmd '.fullschema'

nov: lint
	python3 ./build.py index ${TEST_REPO_DIR}
	@echo
	python3 ./build.py info .

# python3 ./build.py ${TEST_REPOS_DIR}
