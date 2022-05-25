git rev-list --objects --all --tags='0.8' -n5 \
| git cat-file --batch-check='%(objectname) %(objecttype) %(rest)' \
| grep '^[^ ]* blob'
# | cut -d" " -f1,3-
