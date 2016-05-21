# INSTALL

    sudo apt install -y exuberant-ctags python-dev python-virtualenv
    virtualenv ./venv
    . ./venv/bin/activate
    pip install -r ./requirements.txt
    cd ./shotglass
    ./manage.py migrate


# DEMO: Flask, a small project

Shotglass displays information about all source files in a large project. For each file, it renders a single dot per line of code. If code has a symbol definition, ...

Overall workflow:

- get source
- find interesting source files, put in a list
- use "ctags" to find symbols and other info about listed files
- store symbols in database index for quick processing

    # get source
    $ apt source python-flask
    $ ./manage.py make_index --project=flask \
    --prefix=`echo ../../test-projects/Flask*` --tags=flask.tags

    $ ./manage.py show flask
    project        syms   max  avg  total
    flask           402   196   10   4121

    $ ./manage.py render flask
    $ firefox flask_path.png

![Flask](images/flask_path.png)


# DEMO: Django, a bit larger

    $ apt source python-django
    $ find ./python-django-*/django \
    | egrep -v '/(contrib|debian|conf/locale|\.pc|tests)/' > django.lst
    $ ctags --fields=afmikKlnsStz --languages=python -L django.lst -o django.tags
    $ ./manage.py make_index --project=django --prefix=$PWD/python-django* --tags=django.tags

    $ ./manage.py show django
    project        syms   max  avg  total
    django         6664   335    8  53511

    $ ./manage.py render django

![Django](images/django_path.png)

# MORE DEMOS

## Tags mode

In "tags mode", a source tree is colored per tag, or directory.  Since
Flask has only one directory, it's not that interesting:

![Flask](images/flask_tags.png)
