SRCDIR := ../../test-projects
VBIN := $(VIRTUAL_ENV)/bin
CTAGS := ctags --fields=afmikKlnsStz 
all:

flask:
	$(CTAGS) -o $@.tags --recurse --exclude=examples --exclude=testsuite $(SRCDIR)/Flask* 
	$(VBIN)/python ./manage.py make_index \
	--project=$@ --prefix=$(SRCDIR)/Flask* --tags=$@.tags
	$(VBIN)/python ./manage.py show --project=$@

postgres:
	find $(SRCDIR)/postgres*/src -name '*.c' \
	| egrep -v '/(interfaces|port|test)/' > $@.lst
	$(CTAGS)  -L $@.lst
	$(VBIN)/python ./manage.py make_index --project=$@ --prefix=$(SRCDIR)/postgres*
	$(VBIN)/python ./manage.py show --project=$@

redis:
	find $(SRCDIR)/redis* -name '*.c' \
	| egrep -v '(tests|utils)' > $@.lst
	$(CTAGS) -L $@.lst
	$(VBIN)/python ./manage.py make_index --project=$@ --prefix=$(SRCDIR)/redis*
	$(VBIN)/python ./manage.py show --project=$@

xv6:
	ctags --fields=afmikKlnsStz $(SRCDIR)/xv6/*.c
	$(VBIN)/python ./manage.py make_index --project=xv6 --prefix=$(SRCDIR)/xv6

linux1:
	$(CTAGS) `$$(find $(SRCDIR)/linux -name '*.c')`
	$(VBIN)/python ./manage.py make_index --project=linux1 --prefix=$(SRCDIR)/linux
	$(VBIN)/python .manage show --project=$@

linux3:
	find $(SRCDIR)/linux-3* -name '*.c' | egrep -v '/(drivers|scripts)/' \
	| egrep -v '/net/(appletalk|ax25|decnet|ipv6|irda|sctp)' \
	| egrep -v '/fs/(ceph|xfs)' | egrep -v /codecs/ \
	| egrep -v 'kernel/cpu/.+/' > $@.lst
	$(CTAGS) -L $@.lst
	$(VBIN)/python ./manage.py make_index \
	--project=$@ --prefix=$(SRCDIR)/linux-3*
	$(VBIN)/python .manage show --project=$@

django:
	find $(SRCDIR)/python-django-1.7.6/django \
	| egrep -v '/(contrib|debian|conf/locale|\.pc|tests)/' \
	> $@.lst
	ctags --fields=afmikKlnsStz --languages=python -L $@.lst
	$(VBIN)/python ./manage.py make_index \
	--project=django --prefix=$(SRCDIR)/python-django-1.7.6/django

allprojects: django xv6 linux1
