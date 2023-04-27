# github_api.py


import os
import re
import requests

# FIXME: make authorized vs public more obvious

def _get_token():
    return os.environ.get('GITHUB_TOKEN')

def is_authorized():
    token = _get_token()
    if not (token and token.startswith('gh')):
        return False
    return True

def get_api_data(url):
    "return JSON from URL"
    headers = {}
    try:
        token = _get_token()
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            'Authorization': f'Bearer {token}'
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
    if repos.startswith('http') or "/" not in repos:
        raise ValueError('repos must be in the form of "user/repo"')
    url = f"https://api.github.com/repos/{repos}"
    return get_api_data(url)


def parse_github_url(url):
    "return 'user/repo' from URL"
    github_pat = re.compile(r'github.com/(.+?/[^/]+)')
    if match := github_pat.search(url):
        return match.group(1)   # "user/repo"
    return None
    