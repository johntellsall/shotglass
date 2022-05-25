# test_commands.py
#
from click.testing import CliRunner

import main


def test_summary():
    runner = CliRunner()
    result = runner.invoke(main.summary, [])
    assert result.exit_code == 0
    assert result.output.startswith("Projects:")
