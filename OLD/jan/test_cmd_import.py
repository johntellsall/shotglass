import cmd_import


def test_git_ls_tree():
    items = list(cmd_import.git_ls_tree("../SOURCE/flask", release="2.0.0"))

    # check the full content of one item
    assert items[0] == {
        "hash": "e32c8029d1860bf40125d8458db3bd1c4d3f4058",
        "path": ".editorconfig",
        "size_bytes": "217",
    }

    # check the last file isn't ignored
    assert "tox.ini" == items[-1]["path"]

    # check "release" is respected
    items = list(cmd_import.git_ls_tree("../SOURCE/flask", release="1.0"))
    assert items[0]["path"] == ".appveyor.yml"
