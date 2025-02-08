import get_source


def test_parse_archive_path():
    output = """
Skipping already downloaded file 'hello_2.10-3.dsc'
Skipping already downloaded file 'hello_2.10.orig.tar.gz'
Skipping already downloaded file 'hello_2.10.orig.tar.gz.asc'
Skipping already downloaded file 'hello_2.10-3.debian.tar.xz'"""
    assert get_source.parse_archive_path(output) == {'name': 'hello', 'path': 'hello_2.10.orig.tar.gz', 'version': '2.10'}