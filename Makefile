all:
	
setup:
	python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt

# https://stackoverflow.com/a/41386937/143880
.PHONY: clean
clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete


pre-push:

pre-commit-code: fmt fastlint

# TODO: make general
SRC_DIR := june
fmt:
	make -C $(SRC_DIR) fmt
fastlint:
	make -C $(SRC_DIR) fastlint
pre-commit:
	# make -C $(SRC_DIR) pre-commit
# fmt:
# 	isort .
# 	black .

# fastlint:
# 	flake8 .
# 	@echo DONE
