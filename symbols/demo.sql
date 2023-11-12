-- "loopm demo.show" -- re-run this file when source changes
--
--   """create table if not exists file (
--         id integer primary key, release, path, hash, size_bytes,
--         project_id,
--         foreign key (project_id) references project (id)
--         )""",
--     """create table if not exists symbol (
--         name, path, line_start, line_end, kind,
--         file_id int,
--         project_id int,
--         foreign key (file_id) references file (id),
--         foreign key (project_id) references project (id)
--         )""",


.mode tabs
.headers on

-- COUNT
select count(*) from file as file_count;
select count(*) from symbol as symbol_count;

-- TEST
select f.path, s.line_start, s.name
from symbol s, file f 
where s.file_id = f.id
and f.path like '%test_logging%';


-- DEFINITION of "route"
-- moved in 6/2023 to src/flask/sansio/scaffold.py NOTE: HEAD only!
-- 2.3.3 = src/flask/scaffold.py
select f.path, s.line_start, s.name
from symbol s, file f 
where s.file_id = f.id
and s.name='route';
