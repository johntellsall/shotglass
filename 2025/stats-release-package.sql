select count(*) from sgalpinepackage;

select 'Count-Min-Max of Alpine Releases';
select count(distinct alpine_release) from sgalpinepackage;
select min(alpine_release), max(alpine_release) from sgalpinepackage;

select 'Package Count (all releases)';
select count(*) from sgalpinepackage;

select 'All data';
select alpine_release, pkgname from sgalpinepackage;

-- CREATE TABLE sgalpinepackage (
--         id INTEGER NOT NULL, 
--         alpine_release VARCHAR NOT NULL, 
--         pkgname VARCHAR NOT NULL, 
--         pkgdesc VARCHAR NOT NULL, 
--         pkgver VARCHAR NOT NULL, 
--         pkgrel VARCHAR NOT NULL, 
--         sg_file_num_lines INTEGER, 
--         PRIMARY KEY (id)