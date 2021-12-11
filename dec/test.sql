select distinct(name) from projects;
select '';

select name, path
from projects join files on projects.id = files.project_id
limit 3;
select '';

select 'TODO: for each project, file count';
select name, count(*) from projects
limit 3;
select '';

select tag, creator_dt from releases limit 3;
select '';

select tag, date(creator_dt) from releases limit 3;
select '';


-- select strftime('%m', creator_dt) as month,
-- count(*) as num_releases,
-- strftime('%Y', creator_dt) as year
-- from releases
-- where year >= 2000
-- group by 1

-- select strftime('%Y', creator_dt) as year,
-- count(*) as yearly_releases
-- from releases
-- group by 1


-- create table releases (
--     tag text,
--     creator_dt text -- ISO8601

-- select year(admit_date) as year_of_admit,
--   sum(case when gender='Male' then 1 else 0 end)*100/count(*) as Male, 
--   sum(case when gender='Female' then 1 else 0 end)*100/count(*) as Female, 
--   sum(case when homeless='Yes' then 1 else 0 end)*100/count(*) as Homeless
-- from client
-- group by year(admit_date)
