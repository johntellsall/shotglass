# changes.py -- show file changes over time
# - Dnsmasq, 20 samples over 90 releases

from itertools import pairwise
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

def git_ls_tree(proj, tag, filepat):
    cmd = f"git -C {proj} ls-tree -r --name-only '{tag}' {filepat}"
    return run.run(cmd)


def git_diff_stat(proj, tag1, tag2, filepat):
    cmd = f"git -C {proj} diff --stat '{tag1}' '{tag2}' -- {filepat}"
    # Sample input: ' src/arp.c            |    8 +-'
    stat_pat = re.compile(r'''
                          (?P<path>\S+) 
                          .+?
                          (?P<diff>\d+)
                          ''', re.VERBOSE)
    def parse(line):
        match = stat_pat.search(line)
        if match:
            return match.groupdict()
        return None
    lines = run.run(cmd)
    result = [parse(line) for line in lines]
    breakpoint()


def main(paths):
    proj = paths[0]
    tags = sample_tags(proj)
    print(tags)

    final_tag = tags[-1]
    final_paths = git_ls_tree(proj, final_tag, 'src')
    
    tag_pairs = list(pairwise(tags))
    for src_tag, dest_tag in tag_pairs:
        print(f"Changes from {src_tag} to {dest_tag}")
        result = git_diff_stat(proj, src_tag, dest_tag, 'src')
        breakpoint()
        print(result)
   

if __name__ == '__main__':
    main(sys.argv[1:])