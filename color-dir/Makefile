NAME := sizes
PROJECT := ../SOURCE/nginx

all:

fastlint:
	flake8 ./${NAME}.py
	
cycle:
	python ./${NAME}.py --stat ${PROJECT}
	@echo
	python ./${NAME}.py ${PROJECT}
	./imgcat z.png

auto-cycle:
	ls -1 Makefile *.py | entr -c make cycle
