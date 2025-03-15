select count(*) from sgalpinepackage;

.schema sgalpinepackage

select 'Package Versions';
select min(pkgver), max(pkgver) from sgalpinepackage;

select 'APKBUILD line count';
select min(sg_file_num_lines), max(sg_file_num_lines) from sgalpinepackage;