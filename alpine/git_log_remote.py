# git_log_remote.py -- list tags and info from remote git repo
# Supports all Git repos, not just GitHub

import pathlib
import sys
import subprocess
import tempfile


def run(args):
    return subprocess.check_output(args).decode('utf-8')

# FIXME: create new tempdir if cache is for different repos
# - check git_url inside FETCH_HEAD header
def get_tag_info(git_url, datadir):
    has_cache = pathlib.Path(datadir, "HEAD").exists()
    temp_gitdir = f'--git-dir={datadir}'
    if not has_cache:
        run(['git', temp_gitdir, 'init'])
        out = run(['git', temp_gitdir, 'fetch', '--tags', '--prune', git_url]) 
        print(out)
    tag_format = '--format="%(refname:short) %(*authordate) %(subject)"'
    out = run(['git', temp_gitdir, 'tag', '-l', tag_format])
    return out


def main(repos_url):
    print(repos_url)
    cached = False
    if cached:
        tmpdir = '/tmp/test_remote'
        tag_lines = get_tag_info(repos_url, tmpdir)
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            tag_lines = get_tag_info(repos_url, tmpdir)
    print(tag_lines)

# 	git --git-dir=/tmp/tmux log --date=iso --pretty=format:'%ad %S %s' \
# 		$$(cat z)


if __name__ == '__main__':
    main(sys.argv[1])