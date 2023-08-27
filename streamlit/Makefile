all:

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -qr requirements.txt

.PHONY: %.plot
%.plot: %.py setup
	venv/bin/streamlit run $<