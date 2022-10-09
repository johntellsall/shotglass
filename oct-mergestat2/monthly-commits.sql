-- using sqlite, count monthly commits

-- table commits has this structure:
-- {"author_email":"davidism@gmail.com","author_name":"David Lord","author_when":"2022-10-04T20:09:06-07:00","committer_email":"noreply@github.com","committer_name":"GitHub","committer_when":"2022-10-04T20:09:06-07:00","hash":"3dc6db9d0cfddcfb971c382b014bb56ac3761d3c","message":"Merge pull request #4835 from TehBrian/2.2.x\n\nfix typo in quickstart","parents":2}

select strftime('%Y-%m', author_when) as month, count(*) as commits
from commits
group by month
order by month;

