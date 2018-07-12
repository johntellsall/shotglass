all:

build-all:
	./make_index.py ~/jsrc/shotglass/SOURCE/[a-z]*

rebuild-all: zap-pickles build-all

zap-pickles:
	-$(RM) *.pkl
