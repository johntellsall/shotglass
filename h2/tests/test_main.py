import main

SOURCE = '../SOURCE/dnsmasq'


def test_ls_tree():
    repo = main.GitRepo(SOURCE)
    items = list(repo.ls_tree("HEAD"))
    breakpoint()
    assert len(items) > 0
    for item in items:
        assert "hash" in item
        assert "path" in item
        assert "size_bytes" in item