IMGCAT := imgcat-iterm2 --legacy

all:

run:
	uv run extreemap.py
	${IMGCAT} extreemap.png

getcode:
	uv run extract-nb.py extreemap.ipynb z.py
