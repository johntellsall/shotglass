# github_api.py

# curl -L \
#   -H "Accept: application/vnd.github+json" \
#   -H "Authorization: Bearer <YOUR-TOKEN>"\
#   -H "X-GitHub-Api-Version: 2022-11-28" \
#   https://api.github.com/repos/OWNER/REPO/releases


import json
import requests

def get_api_data(url):
    try:
        return json.loads(urllib.request.urlopen(url).read().decode())
    except urllib.error.HTTPError as err:
        print('HTTPError:', err, url)
        return None


def get_github_releases(repos):
    assert "/" in repos, 'repos must be in the form of "user/repo"'
    url = f"https://api.github.com/repos/{repos}/releases"
    url += "?per_page=100"
    return get_api_data(url)
