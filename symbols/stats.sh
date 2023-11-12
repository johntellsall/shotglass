#!/usr/bin/env bash

# stats.sh -- print stats about a Git project
# FIXME: handle other languages

set -euo pipefail # strict mode

PROJECT_DIR=$1

cd ${PROJECT_DIR}

FILES=$(git ls-files | wc -l)
PY_FILES=$(git ls-files '*.py' | wc -l)
PY_LOC=$(wc -l $(git ls-files '*.py') | tail -1)

echo "${PROJECT_DIR}:"
echo "files: ${FILES} python files: ${PY_FILES} -> ${PY_LOC} LOC"