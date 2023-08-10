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


-- XX Middle Released Packages (90+ days per release)
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
    having num_releases > 5 and days_per_release between 14+1 and 90-1;


-- XX Packages tagged by Release Frequency
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
        having num_releases > 5
    )
    select * from BLOB;



    -- strftime('%Y-%m-%d', min(release_created_at)) as first_release,
    -- strftime('%Y-%m-%d', max(release_created_at)) as latest_release,
    -- count(*) as num_releases,

    -- "biweekly" if 14 days or less
    -- case when days_per_release <= 14 then 'biweekly'
    -- else 'OTHER' end as release_frequency 

    -- "monthly" if 30 days or less
    -- when days_per_release <= 30 then 'monthly'
    -- -- "quarterly" if 90 days or less
    -- when days_per_release <= 90 then 'quarterly'
    -- -- "semiannual" if 180 days or less
    -- when days_per_release <= 180 then 'semiannual'
    -- -- "annual" if 365 days or less
    -- when days_per_release <= 365 then 'annual'
    -- otherwise "inactive"
    -- else 'inactive' end as release_frequency 

    -- from github_releases, days_per_release
    -- group by package
    -- having num_releases > 5;

