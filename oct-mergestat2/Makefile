all:

monthly.csv: monthly-commits.sql
	cat monthly-commits.sql | mergestat \
    --repo ../SOURCE/flask \
    --format=csv > $@
	@echo
	head -n 5 $@

.PHONY: monthly.csv
