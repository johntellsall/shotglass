from pathlib import Path
import sys
import run


def proj_list_paths(projtop):
    def is_boring(path):
        return 'contrib/' in path
    
    base = Path(projtop)
    orig_paths = run.git_ls_files(projtop, 'HEAD', '**/*.c')
    rel_paths = [path for path in orig_paths if not is_boring(path)]

    paths = [base / relpath for relpath in rel_paths]
    return paths

def parse_git_blame(lines):
    item = {}
    for line in lines:
        if not item:
            words = line.split()
            commit_sha, _, line_num = words[:3]
            # NOTE: group size ignored
            item = dict(commit_sha=commit_sha, line_num=line_num)
        elif not line.startswith('\t'):
            # header
            if line == 'boundary':
                pass
            else:
                hname, hvalue = line.split(None, 1)
                item[hname] = hvalue
        else:
            # content
            yield item
            item = {}

# git -C ../SOURCE/dnsmasq blame -t --line-porcelain
# HEAD -- src/arp.c

def run_git_blame(projtop, rel_paths):
    assert len(rel_paths) == 1
    test_path = rel_paths[0]
    cmd = f'git -C {projtop} blame -t --line-porcelain HEAD -- {test_path}'
    lines = run.run(cmd)
    return parse_git_blame(lines)


def main(proj_list):
    for projtop in proj_list:
        name = Path(projtop).stem
        paths = proj_list_paths(projtop)
        print(f'{name}: {len(paths)} source files')

        symbols = list(run.run_ctags(paths))
        print(f'{name}: {len(symbols)} symbols')

        sym_paths = {sym['path'] for sym in symbols}
        sym_paths = [Path(sym_path).relative_to(projtop) for sym_path in sym_paths]

        for spath in sym_paths:
            print(f'** {spath}')
            blame = list(run_git_blame(projtop, [spath]))
            for bitem in blame:
                print(spath, end='')
                print(':{line_num} {author} {summary}'.format(**bitem))
            # fields = ('author', 'line_num', 'summary')

if __name__ == "__main__":
    main(sys.argv[1:])
