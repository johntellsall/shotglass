-- .schema files

select 'Project File Sizes';

select projects.name as project_name, path, byte_count
from files, projects
on files.project_id = projects.id
where project_id in (1,2)
limit 10;

select '';
select 'Projects';
select '-- C';

select name,size_mb from proj_summary where language='C' and size_mb < 200 order by 2;

select '';
select '-- Python';
select name,size_mb from proj_summary where language='Python' order by 2;
