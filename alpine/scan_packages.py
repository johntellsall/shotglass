import contextlib
import json
import pprint
import sqlite3
import sys
import urllib.request


def get_api_data(url):
    return json.loads(urllib.request.urlopen(url).read().decode())


def get_github_releases(repos):
    assert "/" in repos, 'repos must be in the form of "user/repo"'
    url = f"https://api.github.com/repos/{repos}/releases"
    url += "?per_page=100"
    return get_api_data(url)


def get_github_repos(repos):
    assert "/" in repos, 'repos must be in the form of "user/repo"'
    url = f"https://api.github.com/repos/{repos}"
    url += "?per_page=100"
    return get_api_data(url)


def demo():
    data = get_github_repos("matplotlib/matplotlib")
    pprint.pprint(data)


def main(dbpath):
    with contextlib.closing(sqlite3.connect(dbpath)) as conn:
        for repos in ["matplotlib/matplotlib"]:
            data = get_github_repos(repos)
            print(f"{repos}: {data['topics']}")


if __name__ == "__main__":
    main(sys.argv[1])
