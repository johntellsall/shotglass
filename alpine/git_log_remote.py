# git_log_remote.py -- list tags and info from remote git repo
# Supports all Git repos, not just GitHub

import sys
import subprocess


def run(args):
    return subprocess.check_output(args).decode('utf-8')


# FIXME: create and teardown tempdir
def main(repos_url):
    print(repos_url)
    run(['git', '--git-dir=/tmp/tmux', 'init'])
    out = run(['git', '--git-dir=/tmp/tmux', 'fetch', '--tags', '--prune', repos_url]) 
    print(out)
    out = run(['git', '--git-dir=/tmp/tmux', 'tag', '-l'])
    print(out)

# 	git --git-dir=/tmp/tmux log --date=iso --pretty=format:'%ad %S %s' \
# 		$$(cat z)


if __name__=='__main__':
    main(sys.argv[1])