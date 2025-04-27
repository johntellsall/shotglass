IMGCAT := imgcat-iterm2 --legacy -W 100

all:

run:
	uv run extreemap.py
	${IMGCAT} extreemap.png

getcode:
	uv run extract-nb.py extreemap.ipynb z.py
