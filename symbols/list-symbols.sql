select
s.name,
s.line_end - s.line_start + 1 as line_count,
s.path
from symbol s

where s.path not like 'examples/%'
and s.path not like 'tests/%'

order by 1


-- """create table if not exists symbol (
--         name, path, line_start, line_end, kind,
--         project_id int,