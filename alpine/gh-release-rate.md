# Package Release Rates

## totals

Alpine Linux has XX 1600 packages, of which XX 250 are in GitHub.
XX of those have Releases
XX more than five releases
XX TBD


## frequent releases -- under two weeks average

    package	        first_release	latest_release		num_releases	days_per_release
    protobuf        2019-10-24		2023-08-01 17:27:01	100	            13
    pspg            2019-07-24		2023-08-02 14:20:51	100	            14
    ruby-bundler    2021-11-08		2023-08-02 08:22:42	100	            6

## REFERENCE

Typical SQL:

    .headers on
    .mode tabs
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
    having num_releases > 5 and days_per_release <= 14