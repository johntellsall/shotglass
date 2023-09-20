# git_log_remote.py -- list tags and info from remote git repo
# Supports all Git repos, not just GitHub

import sys
import subprocess


def run(args):
    return subprocess.check_output(args).decode('utf-8')

import tempfile


def get_tag_info(git_url, datadir):
    # FIXME: only fetch if needed
    temp_gitdir = f'--git-dir={datadir}'
    run(['git', temp_gitdir, 'init'])
    out = run(['git', temp_gitdir, 'fetch', '--tags', '--prune', git_url]) 
    print(out)
    # out = run(['git', temp_gitdir, 'tag', '-l'])
    out = run(['git', temp_gitdir, 'tag', '-l', '--format="%(refname:short) %(objectname:short) %(subject)"'])
    print(out)
# 	git --git-dir=/tmp/tmux log --date=iso --pretty=format:'%ad %S %s' \

    return out

# FIXME: create and teardown tempdir
def main(repos_url):
    print(repos_url)
    tmpdir = '/tmp/test_remote'
    # with tempfile.TemporaryDirectory() as tmpdir:
    get_tag_info(repos_url, tmpdir)
        # print(out)

# 	git --git-dir=/tmp/tmux log --date=iso --pretty=format:'%ad %S %s' \
# 		$$(cat z)


if __name__ == '__main__':
    main(sys.argv[1])