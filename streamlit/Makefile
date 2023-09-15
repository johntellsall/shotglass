all:

setup:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -qr requirements.txt

.PHONY: %.run
%.run: %.py setup
	venv/bin/streamlit run $<

loop:
	git ls-files | entr -c make releases_strip.run