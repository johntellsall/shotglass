SELECT a.alpine_release, a.pkgname, a.pkgver, a.pkgrel, d.rank
FROM sgalpinepackage a 
JOIN debianpopcontest d 
ON a.pkgname = d.name 
WHERE a.alpine_release in ('3.0-stable', '3.10-stable', '3.21-stable')
and d.rank <= 5000
and a.pkgname not in ('dpkg', 'debian-archive-keyring', 'debootstrap')
order by a.alpine_release DESC, d.rank;
