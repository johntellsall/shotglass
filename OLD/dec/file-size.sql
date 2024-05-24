-- .schema files

select 'Project File Sizes';
select name,size_mb,language from proj_summary
where size_mb < 200 order by 2;

select '';
select '== Small C Projects';

select projects.name as project_name, path, byte_count
from files, projects, proj_summary psum
on files.project_id = projects.id
and projects.name = psum.name
where language='C' and size_mb < 200
limit 5;

select '';
select '== Python Projects';

select projects.name as project_name, path, byte_count
from files, projects, proj_summary psum
on files.project_id = projects.id
and projects.name = psum.name
where language='Python' and size_mb < 200
limit 5;

select '';
select 'Projects';
select '-- C';

select name,size_mb from proj_summary where language='C' and size_mb < 200 order by 2;

select '';
select '-- Python';
select name,size_mb from proj_summary where language='Python' order by 2;
