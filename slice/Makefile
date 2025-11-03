all:

run:
	uv run main.py ../SOURCE/dnsmasq
drun:
	uv run python3 -m pdb main.py ../SOURCE/dnsmasq

lpblame:
	git -C ../SOURCE/dnsmasq blame -t --line-porcelain \
	HEAD -- src/rfc1035.c 
	
# 	| head -50 | tail -50

blame:
	git -C ../SOURCE/dnsmasq blame -t \
	HEAD -- src/arp.c \
	| rg -v '^committer' | head -150 | tail -50

list:
	git -C ../SOURCE/dnsmasq ls-files '**/*.c' | head

# zoot:
