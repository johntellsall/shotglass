all:

monthly.csv: monthly.sql
	mergestat --repo ../SOURCE/flask < $< --format=csv > $@
	head -5 $@

monthly.png: monthly.plt
	gnuplot $<
	imgcat $@
