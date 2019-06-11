all:

build-all:
	./make_ctags.py ~/jsrc/shotglass/SOURCE/*

rebuild-all: zap-pickles build-all

zap-pickles:
	-$(RM) *.pkl
