all:

run:
	python3 plot.py
	@echo DONE

venv:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

monthly.csv: monthly-commits.sql
	cat monthly-commits.sql | mergestat \
    --repo ../SOURCE/flask \
    --format=csv > $@
	@echo
	head -n 5 $@

.PHONY: monthly.csv
