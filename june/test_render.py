from click.testing import CliRunner
from render import cli


def test_stats():
    runner = CliRunner()
    result = runner.invoke(cli, ["stats", "NOTYET"])
    assert result.exit_code == 0
    assert "lines of interesting symbols" in result.output
