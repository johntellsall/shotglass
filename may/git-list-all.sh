git rev-list --objects --all \
| git cat-file --batch-check='%(objectname) %(objecttype) %(rest)' \
| grep '^[^ ]* blob'
# | cut -d" " -f1,3-
