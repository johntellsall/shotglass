import pytest

import main
from state import queryall


@pytest.fixture(scope="module")
def test_con():
    con = main.raw_add_project(
        "../SOURCE/flask", is_testing=True, only_interesting=True
    )
    return con


def test_release(test_con):
    release_rows = queryall(test_con, sql='select * from release')
    releases = [dict(row) for row in release_rows]
    assert len(releases) >= 1
    assert releases[0]["label"] == "upstream/3.1.2"


def test_file(test_con):
    file_rows = queryall(test_con, sql='select * from file')
    files = [dict(row) for row in file_rows]
    assert len(files) >= 1
    myfile = files[0]
    assert myfile['path'] == 'src/flask/__init__.py'
    assert myfile['release'] == 'upstream/3.1.2'
    assert int(myfile['size_bytes']) > 1000


# def test_xx(mocker):
#     pfilter = mocker.Mock()
#     pfilter.

#     con = main.raw_add_project(
#     "../SOURCE/flask", is_testing=True, 
#     )


# def test_get_json_from_url(mocker):
#     # Create a mock response object and define its behavior
#     mock_response = mocker.Mock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {"mock_key": "mock_response"}

#     # Patch the requests.get method to return the mock response
#     mocker.patch('requests.get', return_value=mock_response)

#     # Call the function under test
#     result = app.get_json_from_url("https://fakeurl.com")

#     # Assertions
#     assert result == {"mock_key": "mock_response"}
#     requests.get.assert_called_once_with("https://fakeurl.com") # Verify call details
