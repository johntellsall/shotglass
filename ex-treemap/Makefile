SOURCE := ~/jsrc/shotglass/SOURCE

all:

test:
	$(RM) flask.pkl
	./make_ctags.py $(SOURCE)/flask
	./make_squarify.py flask.pkl
	bash ~/bin/imgcat ./flask.png

build-all:
	./make_ctags.py $(SOURCE)/*

rebuild-all: zap-pickles build-all

zap-pickles:
	-$(RM) *.pkl

%.png: %.pkl Makefile
	./make_squarify.py $<