all:

test:
	pytest

data:
	venv/bin/python3 ./timeline_data.py
# echo 'select * from timeline order by date asc limit 2' | sqlite3 timeline.db
# echo 'select * from timeline order by date desc limit 2' | sqlite3 timeline.db

plot:
	venv/bin/python3 ./timeline_plot.py
	imgcat timeline.png

run:
	venv/bin/python3 ./timeline_data.py

fastlint:
	flake8 .
	@echo DONE

# setup -- install Python requirements
setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r ./requirements.txt

format:
	venv/bin/isort .
	venv/bin/black .
