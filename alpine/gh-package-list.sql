-- .schema alpine
select package, source from alpine where
source like "%github.com%"
order by package;
