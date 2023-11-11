-- "loopm demo.show" -- re-run this file when source changes

-- FIRST SYMBOL WITH FILE
select s.name, f.path 
from symbol s, file f 
where s.file_id = f.id
limit 1;

-- TESTS
select s.name, f.path 
from symbol s, file f 
where s.file_id = f.id
and f.path like '%test_logging%'
limit 1;

-- COUNT
select count(*) from file;