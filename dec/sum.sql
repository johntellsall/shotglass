select 'Count of files in project';

select projects.name, count(*)
from files, projects on files.project_id=projects.id
group by 1
;

select '';
select 'Bytes in project';

select projects.name, sum(byte_count)
from files, projects on files.project_id=projects.id
group by 1
;
