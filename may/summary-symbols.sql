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

-- TOTAL SYMBOLS
select count(*) from symbol;
select * from symbol limit 3;

-- TOTAL FILES
select count(*) from file;
select * from file limit 3;

-- min, max symbols per file
-- select min(count), max(count) from (
    select file_id, count(*) as count from symbol group by file_id
-- );