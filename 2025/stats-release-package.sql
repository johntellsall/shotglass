select count(*) from sgalpinepackage;

select 'Count-Min-Max of Alpine Releases';
select count(distinct alpine_release) from sgalpinepackage;
select min(alpine_release), max(alpine_release) from sgalpinepackage;

select 'Package Count (all releases)';
select count(*) from sgalpinepackage;

select "Package Count (each relesae)";
select alpine_release, count(*) from sgalpinepackage group by alpine_release order by 1;

select 'Min-Max of Apkbuild sizes';
select min(sg_file_num_lines), max(sg_file_num_lines) from sgalpinepackage;

select '- largest';
select pkgname, sg_file_num_lines from sgalpinepackage
where sg_file_num_lines > 500
and pkgname not like '%$%';

-- select 'All data';
-- select alpine_release, pkgname from sgalpinepackage;

-- CREATE TABLE sgalpinepackage (
--         id INTEGER NOT NULL, 
--         alpine_release VARCHAR NOT NULL, 
--         pkgname VARCHAR NOT NULL, 
--         pkgdesc VARCHAR NOT NULL, 
--         pkgver VARCHAR NOT NULL, 
--         pkgrel VARCHAR NOT NULL, 
--         sg_file_num_lines INTEGER, 
--         PRIMARY KEY (id)