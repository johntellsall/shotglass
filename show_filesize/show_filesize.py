#!/usr/bin/env python

import sys
from git import Repo
from natsort import natsorted

repo = Repo(sys.argv[1])
# tags = [t.name for t in repo.tags]
for tag in natsorted(repo.tags, key=lambda t: t.name):
    print(tag.name, tag.commit.stats.total)
# tags = ['0.4', '0.8', '0.12.2']
# import ipdb ; ipdb.set_trace()
