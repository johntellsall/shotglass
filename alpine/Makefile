DBPATH := ../shotglass.db
SAMPLE_REPOS := ../SOURCE/flask

all:


# :::::::: RENDER

plot:
	python3 plot.py $(DBPATH)
	
# :::::::: DATABASE MANAGE

nuke_dbsetup:
	-$(RM) $(DBPATH)
	make dbsetup
	
dbsetup:  ## setup database with tables
	python3 dbsetup.py $(DBPATH)
	sqlite3 -echo $(DBPATH) '.tables'

dbimport:  ## import Alpine packages (APKBUILD) info into database
	python3 import_alpine.py $(DBPATH)

scan_releases:
	python3 ./scan_github_releases.py $(DBPATH)


# :::::::: DATABASE QUERY / EXAMPLES

list_versions:  ## list major, minor, and latest versions of packages
	python3 ./list_versions.py $(DBPATH)

summarize_tags:
	python3 ./summarize_tags.py $(DBPATH)

schema:
	sqlite3 -echo $(DBPATH) '.schema *'

show:
	sqlite3 -echo $(DBPATH) '.read show.sql'

ex-list-tags:  ## example: list remote Git tags
	git ls-remote --tags https://github.com/tmux/tmux

ex-list-tags2:
	git --git-dir=/tmp/tmux log --date=iso --pretty=format:'%ad %S %s' 1.0 2.0

ex-list-tags-all:
	git --git-dir=/tmp/tmux tag -l > z
	git --git-dir=/tmp/tmux log --date=iso --pretty=format:'%ad %S %s' \
		$$(cat z)

ex-fetch-tags:
	git --git-dir=/tmp/tmux init
	git --git-dir=/tmp/tmux fetch --tags --prune \
		https://github.com/tmux/tmux
	git --git-dir=/tmp/tmux tag -l

# :::::::: FILESYSTEM

alpine_stats:  ## show subset of package info
	python3 alpine_stats.py aports/main/*

# :::::::: ALPHA

scan_lines0:
	python3 scan_lines.py $(DBPATH) $(SAMPLE_REPOS)
scan_lines:
	python3 scan_lines.py $(DBPATH) $(wildcard ../SOURCE/[a-z]*)

scan_packages:
	python3 scan_packages.py $(DBPATH)
	echo "SUMMARIZE: 'make list-pkg-tags.show'"
# make list-pkg-tags.show

release-dates:
	jq 'map(.name, .tag_name, .created_at)' < releases.json

# :::::::: UTILITIES

sql:
	sqlite3 $(DBPATH)

test:  fastlint ## run Python tests (dev mode: exit on first error)
	PY_SOURCE=$$(git ls-files '*.py') \
	; pytest --exitfirst $${PY_SOURCE}

setup:  ## setup Python virtualenv
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt

distclean:
	-$(RM) -rf venv .pytest_cache

%.show: %.sql  ## run SQL report, send to screen (no output file)
	sqlite3 -echo $(DBPATH) < $<

%.plot: %.py  ## run Seaborn plot, send to screen and file
	python3 $<
	imgcat $(subst plot_,,$(patsubst %.py,%.png,$<))


show-all: $(patsubst %.sql,%.show,$(wildcard *.sql))

fastlint-flake8:
	PY_SOURCE=$$(git ls-files '*.py') \
	; flake8 $${PY_SOURCE}

fastlint:
	PY_SOURCE=$$(git ls-files '*.py') \
	; ruff check $${PY_SOURCE}

fastlint-fix:
	PY_SOURCE=$$(git ls-files '*.py') \
	; ruff check --fix $${PY_SOURCE}

format:
	PY_SOURCE=$$(git ls-files '*.py') \
	; isort $${PY_SOURCE} \
	; black $${PY_SOURCE}

# :::::::: DEMOS

plot_demo_scatter:
	python3 plot_demo_scatter.py
	imgcat plot_demo_scatter.png

plot_github_releases:
	python3 plot_github_releases.py
	imgcat github_releases.png

plot_github_releases2:
	python3 plot_github_releases2.py
	imgcat github_releases2.png

# :::::::: HELPERS

update-alpine:
	cd aports && git pull

clone-alpine:
	git clone --depth=1 https://gitlab.alpinelinux.org/alpine/aports.git

# :::::::: ALSO

zoot:
	python3 ./git_log_remote.py https://github.com/tmux/tmux
zoot2:
	python3 ./git_log_remote.py \
	https://sourceforge.net/projects/zsh/files/zsh/5.9/zsh-5.9.tar.xz