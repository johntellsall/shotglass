.mode tabs
.headers on

-- LIST SYMBOLS IN TEST FILES
-- NOTE: not a great demo with Flask
select f.path, s.line_start, s.name
from symbol s, file f 
where s.file_id = f.id
and f.path like '%test%';

-- EXAMPLE SYMBOLS
select * from symbol limit 5;
