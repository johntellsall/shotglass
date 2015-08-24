SRCDIR := ../../test-projects
VBIN := $(VIRTUAL_ENV)/bin

all:

xv6:
	ctags --fields=afmikKlnsStz $(SRCDIR)/xv6/*.c
	$(VBIN)/python ./manage.py make_index --project=xv6 --prefix=$(SRCDIR)/xv6

linux1:
	find $(SRCDIR)/linux -name '*.c' | xargs wc -l | tail -1
	ctags --fields=afmikKlnsStz $$(find $(SRCDIR)/linux -name '*.c')
	$(VBIN)/python ./manage.py make_index --project=linux1 --prefix=$(SRCDIR)/linux

linux3:
	find $(SRCDIR)/linux-3* -name '*.c' | egrep -v '/(drivers|scripts)/' \
	| egrep -v '/net/(appletalk|ax25|decnet|ipv6|irda|sctp)' \
	| egrep -v '/fs/(ceph|xfs)' | egrep -v /codecs/ \
	| egrep -v 'kernel/cpu/.+/' > linux3.lst
	ctags --fields=afmikKlnsStz -L linux3.lst
	$(VBIN)/python ./manage.py make_index \
	--project=linux3 --prefix=$(SRCDIR)/linux-3*

django:
	find $(SRCDIR)/python-django-1.7.6/django \
	| egrep -v '/(contrib|debian|conf/locale|\.pc|tests)/' \
	> $@.lst
	ctags --fields=afmikKlnsStz --languages=python -L $@.lst
	$(VBIN)/python ./manage.py make_index \
	--project=django --prefix=$(SRCDIR)/python-django-1.7.6/django

allprojects: django xv6 linux1
