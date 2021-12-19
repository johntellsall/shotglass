.schema files

select '';
select 'Project File Sizes';

select projects.name, path, byte_count
from files, projects
on files.project_id = projects.id
where project_id in (1,2) limit 3;
