
import sys


def main(repos_url):
    print(repos_url)
# git --git-dir=/tmp/tmux init
# 	git --git-dir=/tmp/tmux fetch --tags --prune \
# 		https://github.com/tmux/tmux
# 	git --git-dir=/tmp/tmux tag -l
# git --git-dir=/tmp/tmux tag -l > z
# 	git --git-dir=/tmp/tmux log --date=iso --pretty=format:'%ad %S %s' \
# 		$$(cat z)

if __name__=='__main__':
    main(sys.argv[1])