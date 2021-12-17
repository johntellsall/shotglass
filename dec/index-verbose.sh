#!/usr/bin/env bash

set -euo pipefail # strict mode

SOURCE_DIR="/Users/johnmitchell/jsrc/shotglass/SOURCE"

echo
echo :::::::::::::::::::::::
echo ":: $1"
echo ::

python3 ./build.py index "${SOURCE_DIR}/$1"

python3 ./build.py pinfo $1
