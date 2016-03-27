# INSTALL

    sudo apt install python-dev python-virtualenv
    virtualenv ./venv
    . ./venv/bin/activate
    pip install -r ./requirements.txt
    ./manage.py migrate


# DEMO

    $ apt source python-flask
    $ ./manage.py make_index --project=flask \
    --prefix=`echo ../../test-projects/Flask*` --tags=flask.tags

    $ ./manage.py show flask
    project        syms   max  avg  total
    flask           402   196   10   4121

    $ ./manage.py render flask
    $ firefox flask_path.png

![Flask](images/flask_path.png)
