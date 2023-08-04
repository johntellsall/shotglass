-- create table github_releases_blob (
--     package TEXT, releases_json TEXT

-- NUM OF GITHUB PACKAGES
select count(*) from alpine where source like "%github.com%";

-- NUM OF GITHUB RELEASES
select count(*) from github_releases_blob;
