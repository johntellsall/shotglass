-- create table github_releases_blob (
--     package TEXT, releases_json TEXT
-- create table if not exists github_releases (
--         package TEXT, -- not unique
--         release_name TEXT,
--         release_created_at TEXT -- datetime in ISO 8601
-- TOTAL PACKAGES

select count(*) from alpine;

-- NUM OF GITHUB PACKAGES
select count(*) from alpine where source like "%github.com%";

-- NUM WITH GITHUB RELEASES
select count(*) from github_releases_blob;

-- DETAILS: NUM OF PACKAGES
select count(distinct package) from github_releases;
-- DETAILS: NUM OF RELEASES
select count(*) from github_releases;

-- PACKAGE WITH MOST RELEASES
select package, count(*) as num_releases from github_releases
group by package
order by num_releases desc
limit 5;

-- SAMPLE RELEASE DETAILS
select * from github_releases limit 5;
