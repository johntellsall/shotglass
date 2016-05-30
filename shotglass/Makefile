SRCDIR := ../../test-projects
VBIN := $(VIRTUAL_ENV)/bin
CTAGS := ctags --fields=afmikKlnsStz --totals
all:

clean:
	-$(RM) GPATH GRTAGS GSYMS GTAGS

# apt-get source postgresql-9.3 python3.4 python3-flask mysql-common
# apt-get source python2.7 python-django redis
flask:
	find $(SRCDIR)/flask*/flask -name '*.py' \
	| egrep -v '(examples|testsuite|themes)' \
	| $(CTAGS) -L - -o $@.tags
	$(VBIN)/python ./manage.py make_index \
	--project=$@ --prefix=`echo $(SRCDIR)/Flask*` --tags=$@.tags
	$(VBIN)/python ./manage.py show $@

mysql:
	$(CTAGS) -o $@.tags --recurse $(SRCDIR)/mysql*
	wc -l $@.tags
	$(VBIN)/python ./manage.py make_index \
	--project=$@ --prefix=$(SRCDIR)/mysql* --tags=$@.tags
	$(VBIN)/python ./manage.py show $@


postgres:
	find $(SRCDIR)/postgres*/src -name '*.c' \
	| egrep -v '/(interfaces|port|tcl|test|tools|tutorial)/' > $@.lst
	$(CTAGS)  -L $@.lst
	$(VBIN)/python ./manage.py make_index --project=$@ --prefix=$(SRCDIR)/postgres*
	$(VBIN)/python ./manage.py show $@

python2:
	find $(SRCDIR)/python2* -name '*.c' \
	| egrep '/(Objects|Python)/'  > $@.lst
	$(CTAGS)  -L $@.lst
	$(VBIN)/python ./manage.py make_index --project=$@ \
	--prefix=$(SRCDIR)/python2*
	$(VBIN)/python ./manage.py show $@

python3:
	find $(SRCDIR)/python3* -name '*.c' \
	| egrep '/(Objects|Python)/'  > $@.lst
	$(CTAGS)  -L $@.lst
	$(VBIN)/python ./manage.py make_index --project=$@ \
	--prefix=$(SRCDIR)/python3*
	$(VBIN)/python ./manage.py show $@

redis:
	find $(SRCDIR)/redis* -name '*.c' \
	| egrep -v '(tests|utils)' > $@.lst
	$(CTAGS) -L $@.lst
	$(VBIN)/python ./manage.py make_index --project=$@ --prefix=$(SRCDIR)/redis*
	$(VBIN)/python ./manage.py show --project=$@

xv6:
	/bin/ls -1 $(SRCDIR)/xv6/*.c | egrep -v usertests.c \
	| ctags -L - --fields=afmikKlnsStz
	$(VBIN)/python ./manage.py make_index --project=xv6 --prefix=$(SRCDIR)/xv6

linux1:
	$(CTAGS) -o $@.tags `find $(SRCDIR)/linux -name '*.c'`
	$(VBIN)/python ./manage.py make_index \
	--project=linux1 --prefix=$(SRCDIR)/linux --tags=$@.tags
	$(VBIN)/python ./manage.py show $@

linux3-most:
	find $(SRCDIR)/linux-3* -name '*.c' | egrep -v '/(drivers|scripts)/' \
	| egrep -v '/net/(appletalk|ax25|decnet|ipv6|irda|sctp)' \
	| egrep -v '/fs/(ceph|xfs)' | egrep -v /codecs/ \
	| egrep -v 'kernel/cpu/.+/' > $@.lst
	$(CTAGS) -L $@.lst
	$(VBIN)/python ./manage.py make_index \
	--project=$@ --prefix=$(SRCDIR)/linux-3*
	$(VBIN)/python ./manage.py show --project=$@

linux3:
	find $(SRCDIR)/linux-3*/kernel -name '*.c' \
	| egrep -v 'kernel/cpu/.+/' > $@.lst
	$(CTAGS) -L $@.lst
	$(VBIN)/python ./manage.py make_index \
	--project=$@ --prefix=$(SRCDIR)/linux-3*
	$(VBIN)/python ./manage show --project=$@

django:
	find $(SRCDIR)/python-django-*/django \
	| egrep -v '/(contrib|debian|conf/locale|\.pc|tests)/' \
	> $@.lst
	ctags --fields=afmikKlnsStz --languages=python -L $@.lst
	$(VBIN)/python ./manage.py make_index \
	--project=django --prefix=$(SRCDIR)/python-django-*/django

allprojects: django xv6 linux1
