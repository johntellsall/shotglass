-- zap-project.sql

-- select id from projects where name = 'cpython';
delete from projects where name = 'cpython';


-- insert into files (path, byte_count, project_id) values (?, ?, ?)
delete from files
where id in (
    select files.id from files
    join projects on project_id=projects.id
    where projects.name='cpython'
);
-- insert into symbols (file_id, name, start_line, end_line, kind) values (
--     (select id from files where path=?),
-- delete from symbols
-- where id in (
--     select symbols.id from symbols
--     join projects on project_id=projects.id
--     where projects.name='cpython'
-- );
-- select id from symbols where project_id not in (
--     select id from projects
-- );
