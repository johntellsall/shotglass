all:
	@echo
	@echo '######'
	python ./show_filesize.py ../SOURCE/flask/
	@echo '######'
	@echo

testloop:
	fswatch . | xargs -I{} make
