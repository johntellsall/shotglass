-- using sqlite, count commits per month

select
strftime('%Y-%m', author_when) as month,
count(*) as commits
from commits
group by month order by month;
