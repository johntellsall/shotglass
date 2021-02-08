NAME := sizes

all:

cycle:
	python ./${NAME}.py
	./imgcat z.png

auto-cycle:
	ls -1 *.py | entr -c make cycle