## Redis

    gds 2.3-alpha0..3.0-alpha0 '*.c'

  src/dscache.c              |  79 ++++--
   
   src/rdb.c                  | 112 ++++----


# Sort versions, most recent first (Dnsmasq)

    git tag -l --sort=-v:refname | head

    git tag -l --sort=-v:refname | egrep -v '(rc|test)'


# Git diff stat, two versions, only C source

    gds v2.77 v2.78 '*.[ch]'


# Git diff, words only

    gd --word-diff v2.77 v2.78 src/edns0.c
    => [-memcpy(p,-]{+memmove(p,+} p+len+4, rdlen - i);

## also

    gd --word-diff v2.77 v2.78 '*.c'| egrep -v Copyright | egrep '{\+' | less
    
## same, easy to parse

    gd --word-diff=porcelain v2.77 v2.78 src/edns0.c
    -memcpy(p,
	+memmove(p,