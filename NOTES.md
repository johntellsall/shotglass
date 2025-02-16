# NOTES

## GitLab / Debian

* GraphQL is open!

    https://salsa.debian.org/-/graphql-explorer

    * examples
        * query {currentUser {name}}

        * query {
  project(fullPath: "debian/adduser") {
    name
  }
}

* "repos graph"

    https://salsa.debian.org/python-team/packages/matplotlib/-/network/master?ref_type=heads

* Git tags

    https://salsa.debian.org/python-team/packages/matplotlib/-/tags

* repos stats (authors, commit history)

    https://salsa.debian.org/python-team/packages/matplotlib/-/graphs/master/charts

## Misc

* `hello` is 1.5x package size as `dnsmasq`!

## Commands

ls sort by size; default largest first

    ls -sh1 --sort=size *orig.tar*

## Debian

### download popularity contest results

    curl -o by_vote https://popcon.debian.org/by_vote

### all packages mirrored?

Salsa is the Debian GitLab instance. Ex: for package `hello`

Note: extracted! Can browse individual files.

    https://salsa.debian.org/sanvila/hello

### packages point to their Git mirror!

From `apt-get source adduser`:

    NOTICE: 'adduser' packaging is maintained in the 'Git' version control system at:
    https://salsa.debian.org/debian/adduser.git

### DSC example

    Vcs-Browser: https://salsa.debian.org/sanvila/hello
    Vcs-Git: https://salsa.debian.org/sanvila/hello.git

## Alpine

estimate package size before installing (X: check)

    apk search -v --size <package_name>

    apk info --size <package_name>

## Git

Checkout branch, put in worktree directory "beer", keep original Git repos

    git worktree add beer 3.15-stable

# running tests

Flask, with tox, only Python 3.11:

    tox run -e py311

Pass args to Pytest:

    tox run -e py311 -- tests/test_basic.py



# git info on tags and releases

    git tag -n --format='%(refname) %(objecttype)'

Example: Flask

    refs/tags/1.1.0 commit
    refs/tags/1.1.1 commit
    refs/tags/1.1.2 commit
    refs/tags/1.1.3 tag
    refs/tags/1.1.4 tag
    refs/tags/2.0.0 tag

Can use `objectsize` to show rough amount of change... but of tag only? How can we show e.g. "huge code change here / small tweak there"?

Most recent tags

    git for-each-ref refs/tags --sort=-taggerdate --format='%(refname:short)' --count=3

Exclude boring directories

    git diff --stat 3.0.2..3.0.3 | grep -Ev '(.github|requirements|docs)/'

MISC

    git diff --stat 3.0.2..3.0.3



# language-agnostic complexity

* https://github.com/thoughtbot/complexity

# Rendering with Bokeh
- Use "color bars" in Bokeh to do 2D color render
https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html#color-bars

- "box annotations" to colorize different directories https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html#box-annotations
    - or spans https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html#spans

- labels https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html#labels


# Linux Kernel Source
```
git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git
 1557  cd linux-stable/
git checkout v3.0
```
XX doesn't have v2.0 and before


## Needs Upgrading

Following files are Python 2!

make_ver_iproute2.py
make_ver_ansible.py
make_versions.py
app/grid.py
app/management/commands/age.py
app/management/commands/evolve.py
app/management/commands/callscan.py
app/management/commands/label.py
app/management/commands/adjust_index.py
app/management/commands/make_versions.py
app/management/commands/make_ver_postgres.py
app/management/commands/spark.py
app/management/commands/pygdex.py
app/management/commands/sizeplot.py
app/management/commands/words.py
app/management/commands/funcsize.py
app/management/commands/bokplot.py
app/management/commands/draw.py


## GraphQL Salsa Debian GitLab

### list info about 5 projects

query {
  projects(first: 5) {
    nodes {
      id
      name
      description
      webUrl
      visibility
      lastActivityAt
      statistics {
        repositorySize
        storageSize
      }
     
    }
  }
}

### list releases

XX: no results

    query {
  project(fullPath: "debian/adduser") {
    releases(first: 5) {
      nodes {
        tagName
        name
        createdAt
        releasedAt
      }
    }
  }
}