
### Example: Redis table

```bash
./manage.py table --ignore=example --suffixes=c --versions=2.2-alpha0,2.3-alpha0,3.0-alpha0 ../SOURCE/redis/
                                         2.2-alpha0 2.3-alpha0 3.0-alpha0
deps/hiredis/async.c                                   321      321
deps/hiredis/hiredis.c                                1058     1058
deps/hiredis/net.c                                     170      170
deps/hiredis/sds.c                                     479      479
deps/hiredis/test.c                                    479      479
deps/linenoise/linenoise.c                             598      609
src/adlist.c                                  325      325      325
src/ae.c                                      390      390      390
src/ae_epoll.c                                 91       91       91
src/ae_kqueue.c                                93       93       93
src/ae_select.c                                72       72       72
src/anet.c                                    270      347      347
src/aof.c                                     700      646      648
src/config.c                                  438      568      625
src/db.c                                      508      617      618
src/debug.c                                   311      293      293
src/dict.c                                    687      711      712
src/diskstore.c                                        509      509
src/dscache.c                                         1026     1051
src/endian.c                                                     63
src/intset.c                                           422      445
src/lzf_c.c                                   295      295      295
src/lzf_d.c                                   150      150      150
src/multi.c                                   266      264      268
src/networking.c                              594      848      847
src/object.c                                  414      418      418
src/pqsort.c                                  197      197      197
src/pubsub.c                                  267      267      267
src/rdb.c                                     891      998     1014
```

The above table shows three alpha versions and a major version jump. We see:
- the "deps/hires" directory is new to 2.3
- `diskstore.c` appeared in 2.3 and has no changes in version 3.0
- most other files increase or decrease slightly, if there is any change
