all: list

list:
	@echo 'ALPINE TOP'
	find aports/main -type d | rg -v '\.git' | wc -l
	find aports/community -type d | rg -v '\.git' | wc -l
	find aports/testing -type d | rg -v '\.git' | wc -l
# @echo OTHER
# find aports -type d | rg -v '\.git' | rg -v 'aports/(community|main|testing)'

LANG_PAT = '(acf-|apache-mod-|aspell-|clang[0-9]|freeswitch-|font-|lua[0-9]|lua-|perl-|py3-|ruby-)'
LANG_PAT2 = '^lib'
list-main1:
	@echo 'ALPINE MAIN'
	ls -1 aports/main | wc -l
	ls -1 aports/main | rg -v $(LANG_PAT) | wc -l
	ls -1 aports/main | rg -v $(LANG_PAT) | rg -v $(LANG_PAT2) | wc -l


list-main2:
	ls -1 aports/main | rg -v $(LANG_PAT) | rg -v $(LANG_PAT2) \
	| pr --width=140 -6t

list-main: list-main1 list-main2
