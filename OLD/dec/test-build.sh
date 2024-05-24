#!/usr/bin/env bash

set -euo pipefail # strict mode

test -f main.db && rm main.db

echo "=== $1"

time python3 ./build.py index ../SOURCE/$1 | grep '^NUM'

gls -sh main.db
# python3 ./build.py info . | egrep '^NUM'

echo
