all:

# collect -- collect possible tests (fast)
# test -- run all tests
# testloop -- run tests, stop at first err, continue next time
testloop:
	pytest --nbmake  --exitfirst --last-failed "."

test:
	pytest --nbmake  --exitfirst --last-failed "."

collect:
	pytest --collect-only --nbmake "." 

# setup -- install Python requirements
setup:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt
