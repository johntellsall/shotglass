import sqlite3

CREATE_TABLE_STATEMENTS = [
    '''
    CREATE TABLE IF NOT EXISTS project (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS file (
        id INTEGER PRIMARY KEY,
        project_id INTEGER REFERENCES project(id),
        release TEXT,
        path TEXT,
        hash TEXT,
        num_bytes INTEGER,
        num_lines INTEGER, -- TODO: move out
        UNIQUE(project_id, release, path) -- TODO: hash?
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS symbol (
        id INTEGER PRIMARY KEY,
        file_id INTEGER REFERENCES file(id),
        kind TEXT,
        start_line INTEGER,
        end_line INTEGER
    )
    '''
]


def dbsetup(db_path=':memory:'):
    """Create a SQLite database connection and initialize schema."""
    conn = sqlite3.connect(
        db_path,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
    )
    conn.execute('PRAGMA foreign_keys = ON')

    for statement in CREATE_TABLE_STATEMENTS:
        conn.execute(statement)

    conn.commit()
    return conn


def query(db, sql):
    """Run SQL on the database and return the result as a list."""
    cursor = db.cursor()
    cursor.execute(sql)

    if cursor.description is None:
        db.commit()
        return []

    rows = cursor.fetchall()
    return [tuple(row) for row in rows]


def query1(db, sql):
    return query(db, sql)[0][0]