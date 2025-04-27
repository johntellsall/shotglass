IMGCAT := imgcat-iterm2 --legacy -W 100

all:

run:
	uv run active.py
	
run-example:
	uv run extreemap.py
	${IMGCAT} extreemap.png

getcode:
	uv run extract-nb.py extreemap.ipynb z.py
