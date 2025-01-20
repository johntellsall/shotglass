-- pop_over_time.sql -- popularity of packages over time
--
-- SAMPLE:
-- 3.21-stable|tar|1.35|2|59
-- 3.21-stable|e2fsprogs|1.47.1|1|61
-- first col = Alpine release
-- second col = package name
-- third col = package version
-- fourth col = package release
-- fifth col = Debian popularity rank
--
-- NOTE: Sometimes results don't match up well, e.g. "dpkg" very popular in Debian but not in Alpine
-- Also, Alpine-unique packages don't show up in Debian popularity rankings.

SELECT a.alpine_release, a.pkgname, a.pkgver, a.pkgrel, d.rank
FROM sgalpinepackage a 
JOIN debianpopcontest d 
ON a.pkgname = d.name 
WHERE a.alpine_release in ('3.0-stable', '3.10-stable', '3.21-stable')
and d.rank <= 5000
-- remove Debian-isms
and a.pkgname not in ('dpkg', 'debian-archive-keyring', 'debootstrap')
order by a.alpine_release DESC, d.rank;
