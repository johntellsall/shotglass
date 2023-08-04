import json
import pprint

import pytest

import github_api as api


def test_get_api_data():
    response = api.get_api_data("https://jsonplaceholder.typicode.com/todos/1")
    assert "title" in response


@pytest.mark.skipif(not api.is_authorized(), reason="GitHub API key missing or invalid")
def test_get_github_releases():
    response = api.get_github_releases("matplotlib/matplotlib")
    pprint.pprint(response)
    with open("matplotlib_releases.json", "w") as f:
        f.write(json.dumps(response, indent=4))
    assert type(response) is list
    assert "assets_url" in response[0]


@pytest.mark.skipif(not api.is_authorized(), reason="GitHub API key missing or invalid")
def test_get_github_repos():
    response = api.get_github_repos("matplotlib/matplotlib")
    pprint.pprint(response)
    assert "topics" in response


def test_parse_github_url():
    url = "https://github.com/lvc/abi-compliance-checker/archive/$pkgver.tar.gz"
    assert api.parse_github_url(url) == "lvc/abi-compliance-checker"
