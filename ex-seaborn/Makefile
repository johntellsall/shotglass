all:

setup:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

plot.png:
	venv/bin/python plot.py
	imgcat $@

monthly.csv: monthly.sql
	mergestat --repo ../SOURCE/flask < $< --format=csv > $@
	head -5 $@

monthly.png: monthly.plt
	gnuplot $<
	imgcat $@

.PHONY: all setup plot.png monthly.csv monthly.png
