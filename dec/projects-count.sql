select projects.name, count(*)
from files, projects on files.project_id=projects.id
-- where projects.name = 'flask'
-- limit 5
