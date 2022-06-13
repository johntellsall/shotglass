# test_spider.py

from click.testing import CliRunner

from spider import spider


def test_spider():
    runner = CliRunner()
    result = runner.invoke(spider, ["spider.py"])
    assert result.exit_code == 0
    assert "image written" in result.output


def test_blocks():
    runner = CliRunner()
    result = runner.invoke(spider, ["--style=blocks", "spider.py"])
    assert result.exit_code == 0
    assert "image written" in result.output
