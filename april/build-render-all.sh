#!/usr/bin/env bash

set -euo pipefail # strict mode

# for each path given
for path in "$@"; do
    venv/bin/python3 ./shotglass.py build "${path}"
    outpath="temp-$(basename ${path}).png"
    venv/bin/python3 ./shotglass.py render --out="${outpath}"
done