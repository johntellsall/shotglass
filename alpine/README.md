# Packages from Alpine Distro

## NOTES

* set GITHUB_TOKEN in environment to enable GitHub API

Example:

    export GITHUB_TOKEN=$(cat ~/.ssh/github-shotglass.pat)

* needs a lot of work, lots of non-GitHub, non-GitLab sources
  * TODO: parse distinct upstream domains? Ex: cpan, nongnu.org

* code archeology: interesting stats
  * package super old! 6 years!
    * https://gitlab.alpinelinux.org/acf/acf-freeswitch-vmail

  * some packages are super simple -- see "SIMPLE PACKAGES" in `make show.show`

NUM OF PACKAGES PER UPSTREAM
- total 1561
- GitHub 356
- GitLab 71
- other 1134  <==

## All Commands with Examples

### Index

    alpine_stats.py
    dbsetup.py
    github_api.py
    import_alpine.py
    list_versions.py
    plot.py
    plot2.py
    scan_lines.py
    scan_packages.py
    scan_releases.py
    summarize_tags.py

### alpine_stats.py: show subset of package info

Scan filesystem, to verify parsing code.

    python3 alpine_stats.py aports/main/*

    abi-compliance-checker $pkgname-$pkgver.tar.gz::https://github.com/lvc/abi-compliance-checker/archive/$pkgver.tar.gz
    alpine-git-mirror-syncd https://github.com/jirutka/$pkgname/archive/v$pkgver/$pkgname-$pkgver.tar.gz

### dbsetup.py: create database and tables

Create Sqlite database and tables, storing in given file path.

  python3 dbsetup.py temp.db

### import_alpine.py: import Alpine packages into database; show stats

Store data in given Sqlite database file. Output selected stats, like "Number of Packages".

    python3 import_alpine.py ../shotglass.db

    -- TOP 3 PACKAGES BY NUMBER OF FILES
    select * from alpine order by num_files desc limit 3
    package,num_files,build_num_lines,source
    busybox,62,424,https://busybox.net/downloads/busybox-$pkgver.tar.bz2
    gcc,47,794,https://dev.alpinelinux.org/archive/gcc/${_pkgbase%%.*}-${_pkgsnap}/gcc-${_pkgbase%%.*}-${_pkgsnap}.tar.xz

### list_versions: list major, minor, and latest versions of packages

List latest version, and latest major version, of Alpine packages

    python3 ./list_versions.py ../shotglass.db

    jq: 4 tags/releases
      (1, 3, 0) - latest
      (1, 0) - major
 
### scan_github_releases.py: scrape package releases from GitHub

FIXME:

Updates "package_tags" table

Note: uses GitHub API, and takes a while.

    python3 ./scan_releases.py ../shotglass.db

### summarize_tags.py: summarize package database

    python3 ./summarize_tags.py ../shotglass.db

    SUMMARY
    alpine distro:
     - 1561 packages
     - 356 in GitHub
    package_tags:
     - 42226 rows
     - 356 packages
     
### NEEDS WORK: scan_lines.py: count source files and lines

Read files from checked-out Git repos.
Updates database, "package_files_lines" table.

    python3 scan_lines.py ../shotglass.db ../SOURCE/flask
    
    repos=../SOURCE/flask
    name=flask num_files=243 total_lines=35921
    num_packages=22
    5,279 KLOC

### NEEDS WORK: scan_packages.py

Scan GitHub for package name and repos URL.
Updates database, "package_github" table.

    python3 scan_packages.py ../shotglass.db

## Reports

To run a report and output the results to the screen, type `make **myreport**.show` 

### Report Index

    gh-packages.sql
    list-pkg-tags.sql
    nongh-packages.sql
    show.sql

### gh-packages.sql: list details of GitHub packages

    make gh-packages.show

    -- NUM OF GITHUB PACKAGES
    select count(*) from alpine where source like "%github.com%";
    356

    -- LIST OF GITHUB PACKAGES
    select package, num_files from alpine
    where source like "%github.com%"
    order by 1 asc limit 1000;
    abi-compliance-checker|1
    akms|6
    alpine-git-mirror-syncd|1
    alpine-ipxe|6

### list-pkg-tags.sql: list details of packages

    make list-pkg-tags.show

    -- NUMBER OF PACKAGES
    select count(distinct package) from package_tags;
    311

    -- NUMBER OF PACKAGE_TAGS
    select count(*) from package_tags;
    41224

    --  SAMPLE
    select * from package_tags where package like 'darkhttp%' limit 3;
    darkhttpd|v1.13
    darkhttpd|v1.14


### nongh-packages.sql: list non-GitHub packages

    make nongh-packages.show

    -- OTHER
    select count(*) from alpine where
    source not like "%github.com%"
    and source not like "%gitlab.%";
    1134

    -- LIST OF OTHER
    select source from alpine where
    source not like "%github.com%"
    and source not like "%gitlab.%"
    limit 20;
    source
    aaudit-common.lua

### show.sql: more stats

    make show.show

    -- NUMBER OF PACKAGES
    select count(*) from alpine;
    1561

    -- PACKAGE SAMPLE
    select * from alpine limit 3;
    package|num_files|build_num_lines|source
    aaudit|9|52|aaudit-common.lua
    abi-compliance-checker|1|20|$pkgname-$pkgver.tar.gz::https://github.com/lvc/abi-compliance-checker/archive/$pkgver.tar.gz

    -- COMPLEX BUILDS
    select * from alpine order by build_num_lines desc limit 4;
    package|num_files|build_num_lines|source
    gcc|47|794|https://dev.alpinelinux.org/archive/gcc/${_pkgbase%%.*}-${_pkgsnap}/gcc-${_pkgbase%%.*}-${_pkgsnap}.tar.xz
    xen|18|661|https://downloads.xenproject.org/release/xen/$pkgver/xen-$pkgver.tar.gz
    samba|17|612|


## Database Schema

GOAL: represent package releases over time. Example: 1,600 packages from Alpine Linux distro.

### Terms

Package: name, like "jq"
- related: Repos (full source code, often in GitHub)
Release: Package release ID, often like "1.99.2" but no standard format
Tag: Git version control tag, generally more than Releases

