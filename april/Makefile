# flask 10 KLOC
# nginx 186 KLOC
SOURCE_MIN := ../SOURCE/flask
SOURCE_MED := ../SOURCE/nginx

all:

run: run-min run-all

run-min: ## run on simplest/shortest project
	venv/bin/python3 ./shotglass.py $(SOURCE_MIN)

run-medium:
	venv/bin/python3 ./shotglass.py $(SOURCE_MED)

run-all:
	venv/bin/python3 ./shotglass.py ../SOURCE/{coreutils,dnsmasq,flask,nginx,iproute2}

setup:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt
