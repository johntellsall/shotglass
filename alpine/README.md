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

### alpine_stats.py: show subset of package info

    python3 alpine_stats.py aports/main/*
    
    abi-compliance-checker $pkgname-$pkgver.tar.gz::https://github.com/lvc/abi-compliance-checker/archive/$pkgver.tar.gz
    alpine-git-mirror-syncd https://github.com/jirutka/$pkgname/archive/v$pkgver/$pkgname-$pkgver.tar.gz

### dbsetup.py: create database and tables

### import_alpine.py: import Alpine packages into database; show stats

    python3 import_alpine.py ../shotglass.db

    -- TOP 3 PACKAGES BY NUMBER OF FILES
    select * from alpine order by num_files desc limit 3
    package,num_files,build_num_lines,source
    busybox,62,424,https://busybox.net/downloads/busybox-$pkgver.tar.bz2
    gcc,47,794,https://dev.alpinelinux.org/archive/gcc/${_pkgbase%%.*}-${_pkgsnap}/gcc-${_pkgbase%%.*}-${_pkgsnap}.tar.xz

### list_versions: list major, minor, and latest versions of packages

    numactl: 35 tags/releases
      (2, 0, 9) - latest
      (2, 0) - major
      (1, 0) - major
    oniguruma: 1 tags/releases
      (5, 9, 6) - latest
      
scan_lines.py
scan_packages.py
scan_releases.py
summarize_tags.py
test_alpline_stats.py
test_list_versions.py
