import run

CTAGS_KEYS = {
    "_type",
    "name",
    "path",
    "access",
    "inherits",
    "language",
    "line",
    "kind",
    "roles",
    "end",
}


def test_run_ctags():
    res = list(run.run_ctags(path="sample_code/sample.py"))
    assert set(res[0]) == CTAGS_KEYS
