import get_source


def test_parse_archive_path():
    output = """
Skipping already downloaded file 'hello_2.10-3.dsc'
Skipping already downloaded file 'hello_2.10.orig.tar.gz'
Skipping already downloaded file 'hello_2.10.orig.tar.gz.asc'
Skipping already downloaded file 'hello_2.10-3.debian.tar.xz'"""
    assert get_source.parse_archive_path(output) == {'name': 'hello', 'path': 'hello_2.10.orig.tar.gz', 'version': '2.10'}

def test_parse2():
    output = """
Get:2 https://deb.debian.org/debian bookworm/main hello 2.10-3 (tar) [726 kB]
"""
    assert get_source.parse_archive_path(output) == {'name': 'hello', 'version': '2.10'}
    # 'path': 'hello_2.10.orig.tar.gz', 