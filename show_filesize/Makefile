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
index-all:
	./show_info.py ~/src/SOURCE/*
# XX skip large Mongo repos
index:
	./show_info.py ~/src/SOURCE/[^m]*