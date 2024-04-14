SOURCE := ../SOURCE/flask
SOURCE2 := ../SOURCE/dnsmasq

all:

run:
	venv/bin/python3 ./shotglass.py $(SOURCE)

run-real:
	venv/bin/python3 ./shotglass.py $(SOURCE2)

run-all:
	venv/bin/python3 ./shotglass.py ../SOURCE/{coreutils,dnsmasq,nginx,iproute2}

setup:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt
