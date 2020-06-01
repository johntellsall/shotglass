SOURCE := ../SOURCE
PROJ := dnsmasq
NAME := summarize.py

all:

dev:
	PYTEST_ADDOPTS='-sv $(NAME)' pipenv run ptw --clear --verbose
# dev:
# 	PYTEST_ADDOPTS='-sv' pipenv run ptw --clear --verbose
	
index:
	du -sh $(SOURCE)/* | sort -n

.PHONY: projects.csv
projects.csv:
	pipenv run python summarize.py ../SOURCE/[^b]*