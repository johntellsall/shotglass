import main

SOURCE = '../SOURCE/dnsmasq'


def test_ls_tree():
    repo = main.GitRepo(SOURCE)
    items = list(repo.ls_tree("HEAD"))

    assert len(items) > 0
    assert items[0].keys() == {"hash", "path", "size_bytes"}