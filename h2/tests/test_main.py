import main

SOURCE = '../SOURCE/dnsmasq'


def test_ls_tree():
    repo = main.GitRepo(SOURCE)
    items = list(repo.ls_tree("HEAD"))

    assert len(items) > 0
    assert items[0].keys() == {"hash", "path", "size_bytes"}


def test_tag_list():
    repo = main.GitRepo(SOURCE)
    tags = list(repo.tag_list())
    breakpoint()

    assert len(tags) > 0
    assert tags[0].startswith("v")