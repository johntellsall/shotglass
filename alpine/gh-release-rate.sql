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


.headers on
.mode tabs

-- Frequently Released Packages (release biweekly or faster)
    select 
    printf('%-20s', package) as package,
    strftime('%Y-%m-%d', min(release_created_at)) as first_release,
    strftime('%Y-%m-%d', max(release_created_at)) as latest_release,
    count(*) as num_releases,

    cast(
    julianday(max(release_created_at)) - julianday(min(release_created_at))
    as integer) / count(*) as days_per_release

    from github_releases
    group by package
    having num_releases > 5 and days_per_release <= 14;


-- Slowly Released Packages (90+ days per release)
    select 
    printf('%-20s', package) as package,
    strftime('%Y-%m-%d', min(release_created_at)) as first_release,
    strftime('%Y-%m-%d', max(release_created_at)) as latest_release,
    count(*) as num_releases,

    cast(
    julianday(max(release_created_at)) - julianday(min(release_created_at))
    as integer) / count(*) as days_per_release

    from github_releases
    group by package
    having num_releases > 5 and days_per_release >= 90;


-- Packages tagged by Release Frequency
    with BLOB as (
        select
            printf('%-20s', package) as package,
            strftime('%Y-%m-%d', min(release_created_at)) as first_release,
            strftime('%Y-%m-%d', max(release_created_at)) as latest_release,
            count(*) as num_releases,

            cast(
            julianday(max(release_created_at)) - julianday(min(release_created_at))
            as integer) / count(*) as days_per_release
        from github_releases
        group by package
        having num_releases >= 5
    )
    select *,
    case when days_per_release <= 14 then 'biweekly'
    when days_per_release <= 30 then 'monthly'
    when days_per_release <= 90 then 'quarterly'
    when days_per_release <= 180 then 'semiannual'
    when days_per_release <= 365 then 'annual'
    else 'INACTIVE' end as release_frequency 
    from BLOB;

