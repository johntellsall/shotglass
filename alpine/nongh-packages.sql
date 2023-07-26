.schema alpine

-- NUM OF PACKAGES PER UPSTREAM
select count(*) from alpine as total;

select count(*) from alpine where
source like "%github.com%";
select count(*) from alpine where
source like "%gitlab.%";

-- OTHER
select count(*) from alpine where
source not like "%github.com%"
and source not like "%gitlab.%";

-- LIST OF OTHER
select source from alpine where
source not like "%github.com%"
and source not like "%gitlab.%"
order by 1
limit 20;

-- LIST OF GITHUB PACKAGES
select package, source from alpine
where source not like "%github.com%"
and source not like "gitlab.%"
and source > ''
order by 1 asc limit 10;
