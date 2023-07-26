# Packages from Alpine Distro

## NOTES

* package details: https://pkgs.alpinelinux.org/package/edge/main/riscv64/bctoolbox
  * Version	5.1.64-r0
  * Description	Utilities library used by Belledonne Communications softwares like belle-sip, mediastreamer2 and linphone

* package super old! 6 years!
  * https://gitlab.alpinelinux.org/acf/acf-freeswitch-vmail

* needs a lot of work, lots of non-GitHub, non-GitLab sources
  * TODO: parse distinct upstream domains? Ex: cpan, nongnu.org
  * TODO: abandon and code another direction

NUM OF GITHUB PACKAGES PER UPSTREAM
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

    python3 alpine_stats.py aports/main/*

    abi-compliance-checker $pkgname-$pkgver.tar.gz::https://github.com/lvc/abi-compliance-checker/archive/$pkgver.tar.gz
    alpine-git-mirror-syncd https://github.com/jirutka/$pkgname/archive/v$pkgver/$pkgname-$pkgver.tar.gz

### dbsetup.py: create database and tables

### import_alpine.py: import Alpine packages into database; show stats

Store data in given Sqlite database file. Output selected stats, like "Number of Packages".

    python3 import_alpine.py ../shotglass.db

    -- TOP 3 PACKAGES BY NUMBER OF FILES
    select * from alpine order by num_files desc limit 3
    package,num_files,build_num_lines,source
    busybox,62,424,https://busybox.net/downloads/busybox-$pkgver.tar.bz2
    gcc,47,794,https://dev.alpinelinux.org/archive/gcc/${_pkgbase%%.*}-${_pkgsnap}/gcc-${_pkgbase%%.*}-${_pkgsnap}.tar.xz

### list_versions: list major, minor, and latest versions of packages

    python3 ./list_versions.py ../shotglass.db

    numactl: 35 tags/releases
      (2, 0, 9) - latest
      (2, 0) - major
      (1, 0) - major
    oniguruma: 1 tags/releases
      (5, 9, 6) - latest
 
### scan_releases.py: scrape package releases (Git tags)

Updates "package_tags" table

Note: uses GitHub API

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

### gh-package-list.sql: list GitHub packages

    make gh-package-list.show

    abi-compliance-checker|$pkgname-$pkgver.tar.gz::https://github.com/lvc/abi-compliance-checker/archive/$pkgver.tar.gz
    akms|https://github.com/jirutka/akms/archive/v$pkgver/$pkgname-$pkgver.tar.gz
    
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