.mode tabs
.headers on

-- TEST
select f.path, s.line_start, s.name
from symbol s, file f 
where s.file_id = f.id
and f.path like '%test_logging%';

select * from symbol limit 5;
