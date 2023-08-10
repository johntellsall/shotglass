-- create table github_releases (
--     package TEXT, -- not unique
--     release_name TEXT,
--     release_created_at TEXT -- datetime in ISO 8601

-- RELEASE COUNT [tmux]
select count(*) from github_releases where package='tmux';

-- DATE STATS [tmux]
select min(release_created_at), max(release_created_at) from github_releases where package='tmux';

-- DATE RANGE [tmux]
select cast(
    julianday(max(release_created_at)) - julianday(min(release_created_at))
    as integer) as days
from github_releases where package='tmux';

-- AVERAGE DAYS PER RELEASE [tmux]
select cast(
    julianday(max(release_created_at)) - julianday(min(release_created_at))
    as integer) / count(*) as days_per_release
    from github_releases where package='tmux';

-- DATE STATS (all)
.mode tabs
    select package, min(release_created_at), max(release_created_at) from github_releases
    group by package limit 3;
