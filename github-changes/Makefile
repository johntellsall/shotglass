all:

# %.png: %.py
# 	venv/bin/python3 $<

%.show: %.py
	venv/bin/python3 $<
	imgcat $$(ls -1t *.png | head -1)

show:
	make $(shell ls -1t *.py | sed 's/\.py/.show/g' | head -1)

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

