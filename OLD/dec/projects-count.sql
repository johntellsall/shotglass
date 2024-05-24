select '== num files per project';

select projects.name, count(*)
from projects, files  on files.project_id=projects.id
group by projects.name;

select '';
select '== all projects';
select name from projects order by 1;
