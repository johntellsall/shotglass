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

SELECT a.pkgname 
FROM sgalpinepackage a 
JOIN debianpopcontest d 
ON a.pkgname = d.name 
WHERE a.alpine_release = '3.20-stable'
