all:
	
setup:
	python3 -m venv .venv
	.venv/bin/pip install -r ./requirements.txt

# https://stackoverflow.com/a/41386937/143880
.PHONY: clean
clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

distclean: clean
	-$(RM) -rf .venv

# pre-push:

# pre-commit-code: fmt fastlint

# # TODO: make general
# SRC_DIR := june
# fmt:
# 	make -C $(SRC_DIR) fmt
# fastlint:
# 	make -C $(SRC_DIR) fastlint
# pre-commit:
	# make -C $(SRC_DIR) pre-commit
# fmt:
# 	isort .
# 	black .

# fastlint:
# 	flake8 .
# 	@echo DONE

# blobless clone: full history, only HEAD has full files
# git clone --filter=blob:none <url> creates a blobless clone. These clones download all reachable commits and trees while fetching blobs on-demand. These clones are best for developers and build environments that span multiple builds.
# X: kernel.org doesn't obey filter
# clone-linux: URL:=git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git
clone-linux: URL:=https://github.com/torvalds/linux.git
clone-linux:
	git clone --filter=blob:none $(URL) ./SOURCE/linux