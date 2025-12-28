.tables

-- list all user tables and views
select name, type, sql
from sqlite_master
where type in ('table','view')
    -- and name not like 'sqlite_%'
order by name;

select 2+2;