all:

essential-size:
	dpkg-query -Wf '$${Package} $${Essential} $${installed-size}\n' \
	| awk '$$2=="yes" {print $$0}' \
	| sort -k3 -n

# build:
# 	docker build -t jm-debian:bookworm deb-bookworm