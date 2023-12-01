#!/usr/bin/env bash

set -euo pipefail # strict mode

OWNER=johntellsall
REPO=shotglass

curl -L \
    --request GET \
      --url 'https://api.github.com/repos/johntellsall/shotglass/events?since=2023-01-01T00:00:00Z&page=1&per_page=2' 

#   https://api.github.com/repos/${OWNER}/${REPO}/activity

# GITHUB: all events
# curl -i "https://api.github.com/events" \
#   -H "Accept: application/vnd.github.v3+json" \
#   -G --data-urlencode "per_page=10" \
#   --data-urlencode "page=1" \
#   --data-urlencode "since=2023-01-01T00:00:00Z" \
#   --data-urlencode "repo=johntellsall/shotglass"
