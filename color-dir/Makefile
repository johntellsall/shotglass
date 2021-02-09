NAME := sizes

all:

cycle:
	python ./${NAME}.py ../SOURCE/nginx
	./imgcat z.png

auto-cycle:
	ls -1 Makefile *.py | entr -c make cycle