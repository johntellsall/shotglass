# NOTES

## get stats of changes in the last year

* find year-old revision hash

    git rev-list -1 --before='@{1 year ago}' master

-> 1616

* get stat

    git diff --stat HEAD 1616

# OR: get number of added and deleted lines 

gd --numstat  HEAD 1616 '*.[ch]'
0       1       src/core/nginx.c
2       2       src/core/nginx.h
1       2       src/core/ngx_connection.c
2       6       src/core/ngx_cycle.c