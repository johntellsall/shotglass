import git

import may

SAMPLE_PATH = "test_source/sample.py"
CTAGS_SYMBOL = 'Whiskey	test_source/sample.py	5;"	kind:class'


def test_run_ctags():
    ctags_blob = may.run_ctags(SAMPLE_PATH)
    lines = ctags_blob.split("\n")
    assert lines[0] == CTAGS_SYMBOL


def test_parse_ctags():
    tags_iter = may.parse_ctags(CTAGS_SYMBOL + "\n")
    symbol_match = next(tags_iter)
    assert symbol_match.groupdict() == {
        "kind": "class",
        "line_num": "5",
        "name": "Whiskey",
    }


def test_parse_ctags2():
    code = may.run_ctags(SAMPLE_PATH)
    tags_iter = may.parse_ctags(code)

    tags_list = [match["name"] for match in tags_iter]
    assert tags_list == ["Whiskey", "beer", "sip"]


def test_get_project():
    repo = git.Repo("..")
    tree, paths = may.get_project(repo)
    assert type(tree) is git.objects.tree.Tree
    assert len(paths) > 1
    assert all((type(path) is str for path in paths))
