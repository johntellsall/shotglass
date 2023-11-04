-- compare.sql
.schema file
.print

.print "RELEASE 1.9"
.print "-- count:"
select count(*) from file where release='1.9';
select * from file where release='1.9' limit 3;

.print

.print "RELEASE 1.10"
.print "-- count:"
select count(*) from file where release='1.10';
select * from file where release='1.10' limit 3;
