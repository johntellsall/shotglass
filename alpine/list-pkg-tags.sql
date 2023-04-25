.schema package_tags
-- CREATE TABLE package_tags (package TEXT, tag TEXT);

-- NUMBER OF PACKAGES
select count(distinct package) from package_tags;

-- NUMBER OF PACKAGE_TAGS
select count(*) from package_tags;

--  SAMPLE
select * from package_tags where package like 'darkhttp%' limit 3;

-- LARGEST PACKAGES
select package, count(*) from package_tags group by package order by 2 desc limit 5;

-- SMALLEST PACKAGES
select package, count(*) from package_tags group by package order by 2 asc limit 5;

-- ERRORS FIXME:
select package, tag from package_tags where tag like "%error%" limit 5;