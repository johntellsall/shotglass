# test_spider.py

from click.testing import CliRunner
from spider import spider


def test_spider_world():
    runner = CliRunner()
    result = runner.invoke(spider, ["spider.py"])
    assert result.exit_code == 0
    assert "image written" in result.output
