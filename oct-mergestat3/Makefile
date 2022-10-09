all:

monthly.csv: monthly.sql
	mergestat --repo ../SOURCE/flask < $< --format=csv > $@
	head -5 $@
