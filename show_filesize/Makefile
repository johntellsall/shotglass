SOURCE = ~/src/SOURCE/flask

all:
	@echo
	@echo '######'
	@make test
	@echo '######'
	@echo

test:
	./show_info.py ${SOURCE}

testloop:
	fswatch . | xargs -I{} make
