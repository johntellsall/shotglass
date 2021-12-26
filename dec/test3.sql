select 'Count of files in project';

select projects.name, count(*)
from files, projects on files.project_id=projects.id;

select '';
select 'Bytes in project';

select projects.name, sum(byte_count)
from files, projects on files.project_id=projects.id;
