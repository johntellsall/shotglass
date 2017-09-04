FROM python:2.7

RUN apt update
RUN apt install -y \
	exuberant-ctags python-dev 
# nice to have:
RUN apt install -y \
	ack-grep

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /app
    # cd ./shotglass
    # ./manage.py migrate