all:

monthly.csv: monthly.sql
	mergestat --repo ../SOURCE/flask < $<
	@echo DONE
