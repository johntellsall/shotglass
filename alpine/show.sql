.tables
.schema alpine

-- NUMBER OF PACKAGES
select count(*) from alpine;

-- PACKAGE SAMPLE
select * from alpine limit 3;

-- COMPLEX BUILDS
select * from alpine order by build_num_lines desc limit 4;

-- LOTS OF PATCHING
select * from alpine order by num_files desc limit 4;

-- SIMPLE PACKAGES
select * from alpine order by num_files*10 + build_num_lines asc limit 10;

-- AVERAGE BUILD
select avg(build_num_lines) from alpine;

-- NUM OF GITHUB PACKAGES
select count(*) from alpine where source like "%github.com%";
select count(*) from alpine where source like "%alpinelinux%";
