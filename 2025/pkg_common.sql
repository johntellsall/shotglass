-- pkg_common.sql -- find packages in all releases

-- Common: how many releases each package is in
-- select pkgname, count(distinct alpine_release)
-- from sgalpinepackage
-- group by pkgname;

select pkgname from sgalpinepackage
group by pkgname
having count(distinct alpine_release) = (select count(distinct alpine_release) from sgalpinepackage);

select alpine_release, sum(sg_file_num_lines) as total_lines
from sgalpinepackage
group by alpine_release;

-- select 'DONE';
-- CREATE TABLE sgalpinepackage (
--         id INTEGER NOT NULL, 
--         alpine_release VARCHAR NOT NULL, 
--         pkgname VARCHAR NOT NULL, 
--         pkgdesc VARCHAR NOT NULL, 
--         pkgver VARCHAR NOT NULL, 
--         pkgrel VARCHAR NOT NULL, 
--         sg_file_num_lines INTEGER, 