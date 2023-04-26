import github_api as api

def test_get_api_data():
    response = api.get_api_data("https://example.com")
    assert 0, response