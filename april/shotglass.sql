-- shotglass.sql
-- sample: project="flask" path="beer.py" line_count=123
create table
    shotglass (
        id integer primary key autoincrement,
        project text,
        path text,
        line_count integer
    );

-- tag: {"_type": "tag", "name": "scan_projects", "path": "./shotglass.py", "pattern": "/^def scan_projects(con, source_dirs):$/", "language": "Python", "line": 49, "kind": "function", "access": "public", "signature": "(con, source_dirs)", "roles": "def", "end": 54}
create table
    tag (
        id integer primary key autoincrement,
        --     shotglass_project text,
        shotglass_path text,
        _type text,
        name text,
        path text, -- FIXME: compare with shotglass_path
        -- pattern text, -- don't care about pattern
        language text,
        line integer,
        kind text,
        access text,
        signature text,
        roles text,
        end integer
    );