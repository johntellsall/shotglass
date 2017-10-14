FROM python:2.7

RUN apt update
RUN apt install -y \
	exuberant-ctags python-dev 
# nice to have:
RUN apt install -y \
	ack-grep

RUN git clone https://github.com/universal-ctags/ctags.git
RUN cd ctags ; ./autogen.sh ; ./configure ; make install

WORKDIR /app

COPY ./requirements.txt /tmp/
RUN pip install --upgrade pip
# X: sparklines requires 'future'
RUN pip install future
RUN pip install -r /tmp/requirements.txt

WORKDIR /app/shotglass
# COPY . /app
    # cd ./shotglass
    # ./manage.py migrate