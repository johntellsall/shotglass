-- summary-symbols.sql
-- Summarize info from symbols database

--  """create table if not exists project (
--         id integer primary key, name
--         )""",
--     """create table if not exists release (
--         label, project_id,
--         foreign key (project_id) references project (id)
--         )""",
--     """create table if not exists file (
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


-- FILES: COUNT, SAMPLE
select count(*) from file;
select * from file limit 3;

-- SYMBOLS: COUNT, SAMPLE
select count(*) from symbol;
select * from symbol limit 3;

select name,path,file_id from symbol order by file_id asc limit 3;
select name,path,file_id from symbol order by file_id desc limit 3;

select count(distinct file_id) from symbol;

-- SYMBOLS: COUNT BY FILE
select f.path, count(*) as count
from symbol s, file f
where s.file_id = f.id
group by f.path
limit 3;
