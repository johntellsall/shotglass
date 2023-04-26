import pprint
import github_api as api

def test_get_api_data():
    response = api.get_api_data("https://jsonplaceholder.typicode.com/todos/1")
    assert 'title' in response

def test_get_github_releases():
    response = api.get_github_releases("matplotlib/matplotlib")
    pprint.pprint(response)
    assert type(response) is list
    assert 'assets_url' in response[0]

def test_get_github_repos():
    response = api.get_github_repos("matplotlib/matplotlib")
    pprint.pprint(response)
    assert 'topics' in response