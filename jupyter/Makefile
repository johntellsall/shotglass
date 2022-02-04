all:

test:
	pytest --nbmake  --exitfirst --last-failed "."

collect:
	pytest --collect-only --nbmake "." 

setup:
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt
