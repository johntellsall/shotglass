SOURCE := ../SOURCE
PROJ := dnsmasq

all:

dev:
	PYTEST_ADDOPTS='-sv' pipenv run ptw --clear --verbose
	
index:
	du -sh $(SOURCE)/* | sort -n
