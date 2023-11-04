"test main -- outer-level commands"

from click.testing import CliRunner

import main

FLASK_DIR = "../SOURCE/flask/src/flask"
SAMPLE = "sample_code/test_code.py"


def test_ls_tags():
    "test list Git tags in project"
    runner = CliRunner()
    result = runner.invoke(main.ls_tags, [FLASK_DIR])
    assert result.exit_code == 0
    assert "'0.10.1'," in result.output


def test_ctags():
    "test list Ctags e.g. symbol/function information"
    runner = CliRunner()
    result = runner.invoke(main.ctags, [SAMPLE])
    assert result.exit_code == 0
    assert "'kind': 'function'," in result.output
