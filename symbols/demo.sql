-- "loopm demo.show" -- re-run this file when source changes
--
--   """create table if not exists file (
--         id integer primary key, release, path, hash, size_bytes,
--         project_id,
--         foreign key (project_id) references project (id)
--         )""",
--     """create table if not exists symbol (
--         name, path, line_start, line_end, kind,
--         project_id int,
--         foreign key (project_id) references project (id)
--         )""",


.mode tabs
.headers on

-- COUNT
select count(*) from file as file_count;
select count(*) from symbol as symbol_count;

-- DEFINITION of "route"
-- moved in 6/2023 to src/flask/sansio/scaffold.py NOTE: HEAD only!
-- 2.3.3 = src/flask/scaffold.py
select s.*, s.line_end - s.line_start + 1 as line_count
from symbol s
where s.name = 'route';

-- Largest symbols by line count
select s.name,
    (s.line_end - s.line_start + 1) as line_count,
    s.path
from symbol s
order by line_count desc, s.name
limit 10;