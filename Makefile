all:
	
setup:
	python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt

# https://stackoverflow.com/a/41386937/143880
.PHONY: clean
clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete


pre-commit: fmt fastlint

# XXXX TODO: make general
fmt:
	make -C april fmt
fastlint:
	make -C april fastlint
# fmt:
# 	isort .
# 	black .

# fastlint:
# 	flake8 .
# 	@echo DONE
