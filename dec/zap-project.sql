-- zap-project.sql

-- DELETE w
-- FROM WorkRecord2 w
-- INNER JOIN Employee e
--   ON EmployeeRun=EmployeeNo
-- WHERE Company = '1' AND Date = '2013-05-06'

--     proj_id = shotlib.select1(cur, f"select id from projects where name = '{name}'")

-- insert into files (path, byte_count, project_id) values (?, ?, ?)
delete from files
where id in (
    select files.id from files
    join projects on project_id=projects.id
    where projects.name='cpython'
)
;
-- insert into symbols (file_id, name, start_line, end_line, kind) values (
--     (select id from files where path=?),
