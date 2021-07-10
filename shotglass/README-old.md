# INSTALL

NEW [2021]
```
    xcode-select --install
    brew install universal-ctags

    ctags --version
# Universal Ctags 5.9.0
```

OLD
```
    sudo apt install -y exuberant-ctags python-dev python-virtualenv
    virtualenv ./venv
    . ./venv/bin/activate
    pip install -r ./requirements.txt
    cd ./shotglass
    ./manage.py migrate

?
    brew install pipenv

```

## Install 2, using Docker

1. install Docker and Docker Compose
2. `docker-compose up`
3. `cd shotglass`
4. `./manage show all`

More detail:
```
$ alias dc='docker-compose'

# kill old containers (optional)
$ docker stop $(docker ps -a -q)

# build containers, run interactively
$ dc run app bash
```

