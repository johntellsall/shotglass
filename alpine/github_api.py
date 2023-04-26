# github_api.py


import os
import re
import requests


def get_api_data(url):
    "return JSON from URL"
    headers = {}
    try:
        GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
        assert GITHUB_TOKEN.startswith('gh')
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            'Authorization': f'Bearer {GITHUB_TOKEN}'
        }
    except KeyError:
        pass

    try:
        return requests.get(url, headers=headers).json()
    except KeyboardInterrupt as err:  # FIXME:
        print('HTTPError:', err, url)
        return None


def get_github_releases(repos):
    assert "/" in repos, 'repos must be in the form of "user/repo"'
    url = f"https://api.github.com/repos/{repos}/releases"
    url += "?per_page=100"
    return get_api_data(url)


def get_github_repos(repos):
    assert "/" in repos, 'repos must be in the form of "user/repo"'
    url = f"https://api.github.com/repos/{repos}"
    return get_api_data(url)

