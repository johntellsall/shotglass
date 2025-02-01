select count(*) from sgalpinepackage;

.schema sgalpinepackage

select min(pkgver), max(pkgver) from sgalpinepackage;
select min(sg_len_build), max(sg_len_build) from sgalpinepackage;
select min(sg_len_install), max(sg_len_install) from sgalpinepackage;
select min(sg_len_subpackages), max(sg_len_subpackages) from sgalpinepackage;