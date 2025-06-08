# changes.py -- show file changes over time
# - Dnsmasq, 20 samples over 90 releases

import re
import sys
import run

def is_tag_interesting(tag):
    return re.fullmatch('v[0-9.]+', tag) is not None

def sample_tags(proj):
    tags = run.git_tag_list(proj)
    tags = [tag for tag in tags if is_tag_interesting(tag)]
    # Pick every tenth tag
    sampled_tags = tags[::10] # FIXME:
    return sampled_tags

def main(paths):
    proj = paths[0]
    tags = sample_tags(proj)
    print(tags)
   

if __name__ == '__main__':
    main(sys.argv[1:])