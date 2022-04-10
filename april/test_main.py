from click.testing import CliRunner

import main

# def test_hello_world():
#     runner = CliRunner()
#     result = runner.invoke(main.hello, ["Peter"])
#     assert result.exit_code == 0
#     assert result.output == "Hello Peter!\n"


def test_ctags():
    res = list(main.run_ctags("test_code.py"))
    assert len(res) == 2
    assert res[0] == {
        "_type": "tag",
        "access": "public",
        "end": 2,
        "kind": "function",
        "language": "Python",
        "line": 1,
        "name": "func1",
        "path": "test_code.py",
        "roles": "def",
        "signature": "(a, b=None)",
    }
