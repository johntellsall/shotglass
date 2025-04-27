#!/usr/bin/env bash

# build.sh -- reset and rebuild Shotglass symbol database

set -euo pipefail # strict mode

source=$1

time uv run ./main.py add-project --reset-db "../SOURCE/${source}"

echo
make pysummary
# echo
# make summary-symbols.show
