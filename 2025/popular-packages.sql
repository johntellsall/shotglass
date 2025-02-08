-- CREATE TABLE sgalpinepackage (
--         id INTEGER NOT NULL, 
--         alpine_release VARCHAR NOT NULL, 
--         pkgname VARCHAR NOT NULL, 
--         pkgdesc VARCHAR NOT NULL, 
--         pkgver VARCHAR NOT NULL, 
--         pkgrel VARCHAR NOT NULL, 
--         sg_complexity INTEGER, 
--         sg_len_install INTEGER, 
--         sg_len_parse_funcs INTEGER, 
--         sg_len_subpackages INTEGER, 
--         PRIMARY KEY (id)
-- );
-- CREATE TABLE debianpopcontest (
--         rank INTEGER NOT NULL, 
--         name VARCHAR NOT NULL, 
--         inst INTEGER NOT NULL, 
--         vote INTEGER NOT NULL, 
--         old INTEGER NOT NULL, 
--         recent INTEGER NOT NULL, 
--         no_files INTEGER NOT NULL, 
--         maintainer VARCHAR NOT NULL, 
--         PRIMARY KEY (name)
-- );

-- select distinct(a.alpine_release) from sgalpinepackage a;

select "ALPINE PACKAGES POPULAR IN DEBIAN";
-- with Debian-specific ones removed

SELECT a.pkgname, d.rank -- , a.pkgdesc
FROM sgalpinepackage a 
JOIN debianpopcontest d 
ON a.pkgname = d.name 
WHERE a.alpine_release = '3.20-stable'
and d.rank <= 5000
and a.pkgname not in ('dpkg', 'debian-archive-keyring', 'debootstrap')
order by d.rank;


