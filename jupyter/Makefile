all:

# collect -- collect possible tests (fast)
# test -- run all tests
# testloop -- run tests, stop at first err, continue next time
testloop:
	pytest --nbmake  --exitfirst --last-failed \
	-k 'not (mongo or nov or mysql or changes \
	or numfiles or coreutils or shotglass)' \
	*.ipynb

test:
	pytest --nbmake *.ipynb

collect:
	pytest --collect-only --nbmake

# setup -- install Python requirements
setup:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt
