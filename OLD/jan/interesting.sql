-- show interesing source paths
select release, path from file_hash
where path like '%.py'
and path not like 'tests/%'
and path not like 'examples/%'
and path not like '%/testsuite/%'
