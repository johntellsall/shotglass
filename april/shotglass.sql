-- shotglass.sql

-- sample: project="flask" path="beer.py" line_count=123

create table shotglass (
    id integer primary key autoincrement,
    project text,
    path text,
    line_count integer
);
