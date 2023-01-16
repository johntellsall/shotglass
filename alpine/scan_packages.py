import json
import pprint
import urllib.request


def get_github_releases(repos):
    assert "/" in repos, 'repos must be in the form of "user/repo"'
    url = f"https://api.github.com/repos/{repos}/releases"
    url += "?per_page=100"
    data = json.loads(urllib.request.urlopen(url).read().decode())
    return data


def main():
    data = get_github_releases("matplotlib/matplotlib")
    pprint.pprint(data)


if __name__ == "__main__":
    main()
