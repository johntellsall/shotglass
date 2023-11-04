all:

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r ./requirements.txt

%.plot: %.py
	venv/bin/python3 -m $(basename $<)

demo:	sunburst-dataframe.plot
