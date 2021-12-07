select tag, creator_dt from releases limit 3;
select '';
select tag, date(creator_dt) from releases limit 3;

-- create table releases (
--     tag text,
--     creator_dt text -- ISO8601

-- select year(admit_date) as year_of_admit,
--   sum(case when gender='Male' then 1 else 0 end)*100/count(*) as Male, 
--   sum(case when gender='Female' then 1 else 0 end)*100/count(*) as Female, 
--   sum(case when homeless='Yes' then 1 else 0 end)*100/count(*) as Homeless
-- from client
-- group by year(admit_date)
