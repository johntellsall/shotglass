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
                          [\s|]+ # whitespace or pipe
                          (?P<diff>\d+)
                          ''', re.VERBOSE)
    def parse(line):
        if 'changed,' in line:
            return None
        match = stat_pat.search(line)
        if match:
            return match.groupdict()
        return None
    lines = run.run(cmd)
    result = [parse(line) for line in lines]
    result = [item for item in result if item is not None]
    return result


def main(paths):
    proj = paths[0]
    tags = sample_tags(proj)
    print(tags)

    final_tag = tags[-1]
    final_paths = git_ls_tree(proj, final_tag, 'src')
    
    tag_pairs = list(pairwise(tags))
    path_rel_diff = {}
    for src_tag, dest_tag in tag_pairs:
        # print(f"Changes from {src_tag} to {dest_tag}")
        result = git_diff_stat(proj, src_tag, dest_tag, 'src')
        # diff[src_tag, dest_tag] = result
        for diff in result:
            key = (diff['path'], src_tag)
            path_rel_diff[key] = diff['diff']

    sep = '-'
    print(f'Tags: {tags}')
    for path in sorted(final_paths):
        print(f"{path:20}", end=' ')
        for tag in tags[:-1]:
            diff = path_rel_diff.get((path, tag))
            if diff:
                print(f'{diff:>4}', end=' ')
            else:
                print(f'{sep:>4}', end=' ')
        print()



   

if __name__ == '__main__':
    main(sys.argv[1:])