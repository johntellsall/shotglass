select '== all releases for one project';

select name, tag, date(creator_dt)
from projects join releases on projects.id = releases.project_id
where name = 'postgres'
and tag like 'REL_%' and tag not like 'REL2%'
and tag not like 'release%'
and tag not like '%ALPHA%'
and tag not like '%beta%'
and tag not like '%RC%'
limit 1000;

select '';
