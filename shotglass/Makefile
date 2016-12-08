SRCDIR := ../../SOURCE
VBIN := $(VIRTUAL_ENV)/bin
# CTAGS := ctags --fields=afmikKlnsStz --totals

all:	test

.PHONY: query.html
query.html:
	source-highlight -o $@ -i \
	SOURCE/django/django/db/models/query.py

source.lst:
	find SOURCE/django/ -name '*.py' \
	| egrep -v '/(bin|contrib|docs|examples|tests)/' \
	> $@
	xargs < source.lst wc -l | tail -1

server:
		while true; do ./manage.py runserver; sleep 15; done

test:
	py.test

clean:
	-$(RM) $$(find . -name '*.pyc')

migrate:
	./manage.py migrate

# index1 -- index short C and Python projects
index1: migrate
	file $(SRCDIR)/* | awk -F: '/directory/ {print $$1}' \
	| egrep '(redis|flask)' \
	| xargs ./manage.py make_index

index-most: migrate
	file $(SRCDIR)/* | awk -F: '/directory/ {print $$1}' \
	| egrep -v linux \
	| xargs ./manage.py make_index

# apt-get source postgresql-9.3 python3.4 python3-flask mysql-common
# apt-get source python2.7 python-django redis
# wget https://github.com/guilleiguaran/xv6/archive/master.zip

# xv6:
# 	/bin/ls -1 $(SRCDIR)/xv6/*.c | egrep -v usertests.c \
# 	| ctags -L - --fields=afmikKlnsStz
# 	$(VBIN)/python ./manage.py make_index --project=xv6 --prefix=$(SRCDIR)/xv6

# linux1:
# 	$(CTAGS) -o $@.tags `find $(SRCDIR)/linux -name '*.c'`
# 	$(VBIN)/python ./manage.py make_index \
# 	--project=linux1 --prefix=$(SRCDIR)/linux --tags=$@.tags
# 	$(VBIN)/python ./manage.py show $@

# linux3-most:
# 	find $(SRCDIR)/linux-3* -name '*.c' | egrep -v '/(drivers|scripts)/' \
# 	| egrep -v '/net/(appletalk|ax25|decnet|ipv6|irda|sctp)' \
# 	| egrep -v '/fs/(ceph|xfs)' | egrep -v /codecs/ \
# 	| egrep -v 'kernel/cpu/.+/' > $@.lst
# 	$(CTAGS) -L $@.lst
# 	$(VBIN)/python ./manage.py make_index \
# 	--project=$@ --prefix=$(SRCDIR)/linux-3*
# 	$(VBIN)/python ./manage.py show --project=$@

# linux3:
# 	find $(SRCDIR)/linux-3*/kernel -name '*.c' \
# 	| egrep -v 'kernel/cpu/.+/' > $@.lst
# 	$(CTAGS) -L $@.lst
# 	$(VBIN)/python ./manage.py make_index \
# 	--project=$@ --prefix=$(SRCDIR)/linux-3*
# 	$(VBIN)/python ./manage show --project=$@

