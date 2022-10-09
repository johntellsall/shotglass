
-- STATS
-- {
--     "additions": 1,
--     "deletions": 1,
--     "file_path": "docs/quickstart.rst"
--   }
  create table stats (
    additions integer,
    deletions integer,
    file_path text
  );

-- FILES
-- {
--     "contents": "root = true\n\n[*]\nindent_style = space\nindent_size = 4»
--     "executable": 0,
--     "path": ".editorconfig"
--   }
  create table files (
    id integer primary key autoincrement,
    path text,
    contents text,
    executable integer
  );

-- REFS
-- {
--     "full_name": "refs/heads/main",
--     "hash": "3dc6db9d0cfddcfb971c382b014bb56ac3761d3c",
--     "name": "main",
--     "remote": null,
--     "target": null,
--     "type": "branch"
--   }
  create tabble refs (
    full_name text,
    hash text,
    name text,
    remote text,
    target text,
    type text
  );

-- COMMITS
-- {
--     "author_email": "davidism@gmail.com",
--     "author_name": "David Lord",
--     "author_when": "2022-10-04T20:09:06-07:00",
--     "committer_email": "noreply@github.com",
--     "committer_name": "GitHub",
--     "committer_when": "2022-10-04T20:09:06-07:00",
--     "hash": "3dc6db9d0cfddcfb971c382b014bb56ac3761d3c",
--     "message": "Merge pull request #4835 from TehBrian/2.2.x\n\nfix typo i»
--     "parents": 2
--   }
  create table commits (
    author_email text,
    author_name text,
    author_when text,
    committer_email text,
    committer_name text,
    committer_when text,
    hash text,
    message text,
    parents integer
  );
