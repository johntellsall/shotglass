#!/bin/bash

set -euo pipefail # strict mode
set +x # verbose

function clone() {
	git clone --depth=1 "$@"
}

cd ../SOURCE

[[ -e django ]] || clone https://github.com/django/django
[[ -e flask ]] || clone https://github.com/pallets/flask.git
[[ -e odoo ]] || clone https://github.com/odoo/odoo.git
[[ -e pyramid ]] || clone https://github.com/Pylons/pyramid.git
[[ -e sqlalchemy ]] || clone https://github.com/zzzeek/sqlalchemy