select 'Count-Min-Max of Alpine Releases';
select count(distinct alpine_release) from sgalpinepackage;
select min(alpine_release), max(alpine_release) from sgalpinepackage;

select 'Package Count (all releases)';
select count(*) from sgalpinepackage;

-- .schema sgalpinepackage

select 'Package Versions';
select min(pkgver), max(pkgver) from sgalpinepackage;

select 'APKBUILD line count';
select min(sg_file_num_lines), max(sg_file_num_lines) from sgalpinepackage;