SOURCE = ~/src/SOURCE/flask

all:
	@echo
	@echo '################################################'
	@make test
	@echo

test:
	./show_info.py ${SOURCE}

testloop:
	fswatch . | xargs -I{} make

# # xindex:
# 	ls -1 ~/src/SOURCE/ | xargs -n1 -I{} -t  ./show_info.py ~/src/SOURCE/{}
index:
	./show_info.py ~/src/SOURCE/*